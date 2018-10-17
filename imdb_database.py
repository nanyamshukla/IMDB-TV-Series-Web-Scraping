
import pymysql




def mysqldb(email, series):
    db = pymysql.connect("localhost","root","password","mysql")

    cursor = db.cursor()

    sql1 = "Create database [IF NOT EXISTS] IMDbDatabase"
       
    
    cursor.execute(sql1)
    db.commit()


    sql4 = "use IMDbDatabase"
       
    cursor.execute(sql4)
    db.commit()
       
    sql2 = "create table [IF NOT EXISTS] userdata(email varchar(100), series varchar(720))"
       
    cursor.execute(sql2)
    db.commit()

    sql3 = "INSERT INTO userdata VALUES ('%s', '%s' )" % (email, series)
       
    cursor.execute(sql3)
    db.commit()

    db.close()