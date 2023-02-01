# Clarity Project Scraper

## Installation
```
git clone https://github.com/ilarionkuleshov/clarity-project-scraper.git
cd clarity-project-scraper/src/python/src
poetry env use <python3.8>
poetry install
```
Configure _.env_ file according to _.env.example_ (DB, RabbitMQ, proxy).

## Usage
To scrape all edr's from https://clarity-project.info/ (in _src/python/src_ directory):
```
poetry run scrapy crawl edr
```
To load _xlsx_ file with edr's to DB (in _src/python/src_ directory):
```
poetry run scrapy xlsx_edr_importer -f <path_to_xlsx_file>
```
To start _PM2_ processes (in _pm2/_ directory):
```
cp pm2.config.example.js pm2.config.js
pm2 start pm2.config.js
```
To export results from DB to _csv_ file (in _src/python/src_ directory):
```
poetry run scrapy finances_csv_exporter
```
Result _csv_ file will be stored in _src/python/src/storage_ directory.