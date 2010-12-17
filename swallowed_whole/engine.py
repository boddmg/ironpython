import clr
clr.AddReference('IronPython')

from IronPython.Hosting import Python

from System import Array, AppDomain, AppDomainSetup
from System.Runtime.Remoting import ObjectHandle
from System.Security import SecurityManager, SecurityZone
from System.Security.Policy import Evidence, Zone

from threading import Thread
from time import sleep


code = """
class C(object): 
    def hello(self):
        print 'hello'
        
    def bad_stuff(self):
        try:
            import System
            System.Diagnostics.Process.Start('C:\\windows\\system32\\calc.exe')
        except Exception, e:
            print 'cannot do that', e

a = C()
"""


class Engine(object):
    
    def run(self):
        domain = self.create_domain()
        
        units = [self.create_engine(domain, code) 
                 for i in range(10)]
        
        threads = []
        for i, (scope, engine) in enumerate(units):
            worker = self.get_worker(scope, engine, i)
            thread = Thread(target=worker)
            threads.append(thread)
        for i, thread in enumerate(threads):
            thread.start()
        
    
    def get_worker(self, scope, engine, i):
        def worker():
            print 'starting', i
            sleep(5)
            self.execute(scope, engine)
        return worker
    
    
    def create_domain(self):
        info = AppDomainSetup()
        info.ApplicationBase = AppDomain.CurrentDomain.BaseDirectory
        info.ApplicationName = 'PythonSwallowedWhole'
        
        evidence = Evidence()
        evidence.AddHostEvidence(Zone(SecurityZone.Internet))
        
        perm_set = SecurityManager.GetStandardSandbox(evidence)
        new_domain = AppDomain.CreateDomain(
            "psw", evidence, info, perm_set, None
        )
        return new_domain
    
    def create_engine(self, new_domain, code):
        runtime = Python.CreateRuntime(new_domain)
        engine = runtime.GetEngine('py')
        scope = engine.CreateScope()
        source = engine.CreateScriptSourceFromString(code)
        
        source.Execute(scope)
        return scope, engine
    
    
    def execute(self, scope, engine):
        a = scope.GetVariableHandle("a")
        empty = Array.CreateInstance(object, 0)
        
        # remote handle to the method
        method = engine.Operations.GetMember(a, 'hello')
        
        # will print 'hello'
        engine.Operations.Invoke(method, empty)
        return
        method2 = engine.Operations.GetMember(a, 'bad_stuff')

        # will print 'cannot do that Request failed.'
        engine.Operations.Invoke(method2, empty)
        