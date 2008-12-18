import clr
from config import config
import re
from System import DBNull

def getDBClasses(dbType):
    parameterPrefix = ':'
    if dbType == 'sqlite':
        try:
            clr.AddReference('System.Data.SQLite')
            from System.Data.SQLite import (
                SQLiteConnection as Connection,
                SQLiteParameter as Parameter)
        except IOError:
            clr.AddReference('Mono.Data.Sqlite')
            from Mono.Data.Sqlite import (
                SqliteConnection as Connection,
                SqliteParameter as Parameter)
    elif dbType == 'postgres':
        clr.AddReference('Npgsql')
        from Npgsql import (
            NpgsqlConnection as Connection,
            NpgsqlParameter as Parameter)
    elif dbType == 'mysql':
        clr.AddReference('MySql.Data')
        from MySql.Data.MySqlClient import (
            MySqlConnection as Connection,
            MySqlParameter as Parameter)
        parameterPrefix = '?'
    elif dbType == 'sqlserver':
        clr.AddReference('System.Data')
        from System.Data.SqlClient import (
            SqlConnection as Connection,
            SqlParameter as Parameter)
        parameterPrefix = '@'
    else:
        raise ValueError('invalid db_type setting: %r' % dbType)
    return Connection, Parameter, parameterPrefix


Connection, Parameter, parameterPrefix = getDBClasses(config.db_type)


def openConnection():
    conn = Connection(config.connection)
    conn.Open()
    return conn


conn = openConnection()


def fixParameters(sql):
    if parameterPrefix != ':':
        sql = re.sub(r':(\w+)', parameterPrefix + r'\1', sql)
    return sql


SAVE_FRIEND_STATEMENT = fixParameters('''
        insert into friends (
            id, screen_name, name, description,
            location, url, image_url)
        values (
            :id, :screen_name, :name, :description,
            :location, :url, :profile_image_url)''')

SAVE_TWEET_STATEMENT = fixParameters('''
        insert into tweets (
            id, created, text, friend_id)
        values (
            :id, :created_at, :text, :friend_id)''')

GET_FRIENDS_STATEMENT = 'select screen_name from friends order by 1'

GET_TWEETS_STATEMENT = fixParameters('''
        select f.screen_name, f.url, f.location, f.name,
            f.image_url, t.created, t.text
        from friends f inner join tweets t
            on f.id = t.friend_id
        where f.screen_name = :friend
            or :friend is null
        order by t.id desc''')


def setParameter(cmd, name, value):
    if value is None:
        value = DBNull.Value
    cmd.Parameters.Add(Parameter(name, value))


def itemExists(table, id):
    cmd = conn.CreateCommand()
    cmd.CommandText = fixParameters('select 1 from %s where id = :id' % table)
    setParameter(cmd, 'id', id)
    return cmd.ExecuteScalar() == 1


friendAttrs = 'id screen_name name description location url profile_image_url'.split()


def makeTweet(reader):
    tweet = {}
    for i in range(reader.FieldCount):
        tweet[reader.GetName(i)] = reader[i]
    return tweet

