# StarACM

## Usage

### Create Table

```bash
cd StarAcmSpider
# 修改数据库连接参数 `MYSQL_CONNECT_STRING`
vim StarAcmSpider/settings.py
# 创建数据表 `solutions`
python3 StarAcmSpider/models.py
```

### sdut

```bash
scrapy crawl sdut
```