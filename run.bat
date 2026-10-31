@echo off
chcp 65001 > nul
cd /d C:\Users\Arash\PycharmProjects\Auto_Sender
.venv\Scripts\python.exe main.py "https://caramelkids.ir/product-category/لباس-پسرانه/" aarash.fathi87@gmail.com --pages 3 >> log.txt 2>&1