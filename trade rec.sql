CREATE DATABASE trade_recommendation;

USE trade_recommendation;

CREATE TABLE live_stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10),
    datetime DATETIME,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume FLOAT
);



