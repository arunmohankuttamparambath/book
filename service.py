from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql


def register(fs_name,ls_name,su_name,email,username,password):
    con = sql.connect("D:\Python_Workspace\Book\mydb\mybook.db")
    cur = con.cursor()
    cur.execute("INSERT INTO t_users (f_name,l_name,s_name,email,u_name,p_word) VALUES (?,?,?,?,?,?)", (fs_name,ls_name,su_name,email,username,password))
    con.commit()
    con.close()

def retrieveUsers(username,password):
	con = sql.connect("D:\Python_Workspace\Book\mydb\mybook.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM t_users WHERE u_name = ? AND p_word = ?",(username,password))
	users = cur.fetchone()
	con.close()
	return users

	
def retrieveId(uids):
	con = sql.connect("D:\Python_Workspace\Book\mydb\mybook.db")
	cur = con.cursor()
	cur.execute('SELECT * FROM t_users WHERE id = ?',(str(uids)))
	users = cur.fetchone() 
	con.close() 
	return users