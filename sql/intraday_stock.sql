CREATE SEQUENCE stock.intraday_stock_seq;
CREATE TABLE stock.intraday_stock (
  id INT NOT NULL DEFAULT nextval('stock.intraday_stock_seq'::regclass),
  no_stock TEXT NULL,
  dt_stock TIMESTAMP NULL,
  vl_open FLOAT NULL,
  vl_close FLOAT NULL,
  vl_high FLOAT NULL,
  vl_low FLOAT NULL,
  vl_adjusted_close FLOAT NULL,
  vl_volume INT NULL,
  CONSTRAINT INTRADAY_STOCK_PK PRIMARY KEY (id)
);