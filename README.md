# tradeX

Paper: http://cs230.stanford.edu/projects_winter_2021/reports/70728801.pdf

Youtube: https://www.youtube.com/watch?v=B3HGXIkQrIw

Models described in paper are located in:
A. ./model/model_lstm256_dropout_dense256_dropout.py
B. ./model/model_lstm512_dropout_dense512_dropout.py
C. ./model/model_lstm128_dropout_dense128_dropout.py
D. ./model/model_lstm256_dense256.py
E. ./model/model_lstm256_dropout_lstm256_dropout_dense256_dropout.py
F. ./model/model_lstm256_dropout_dense256_dropout_dense256_dropout.py

This project trains models to predict long term stock performance based on financial statements.

This is a cs230 project. It contains code blocks of:
1. crawling raw data (balance sheet, income statement, cash flow statement, historical price) from nasdaq.com;
2. parsing raw data into processed data;
3. getting statistics from processed data;
4. using processed data as dataset to train models;

The order of running codes is:
1. to craw data from web:
./crawler/balance_sheet_crawler.py
./crawler/income_statement_crawler.py
./crawler/cash_flow_statement_crawler.py
./crawler/historical_price_crawler.py

2. to parse data into structured items for model training:
./parser/balance_sheet_parser.py
./parser/income_statement_parser.py
./parser/cash_flow_statement_parser.py
./parser/combined_intersection.py
./parser/combined_union.py

3. (optional) to get some statistics from structured items:
./statistics/balance_sheet_filtered_data_statistics.py
./statistics/income_statement_filtered_data_statistics.py
./statistics/cash_flow_statement_filtered_data_statistics.py

4. to train models:
./model/balance_sheet_filtered_data_neural.py
./model/income_statement_filtered_data_neural.py
./model/cash_flow_statement_filtered_data_neural.py
./model/combined_filtered_data_intersection_neural.py
./model/combined_filtered_data_union_neural.py
./model/combined_filtered_data_union_neural_lstm.py
