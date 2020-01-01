# BookToMarkdown
根据书名从豆瓣爬虫转化为 markdown

## 使用方法
```shell
BookToMarkdown.py (-i | -n) -o [-c] [--id]
```

有 2 种搜索模式，一种是根据名称进行模糊搜索，另一种是根据 id 进行精确搜索

`-i`：即 input，指定批量输入的文件路径，可为名称或 id

`-n`：即 name，指定单个输入的文件路径，可为名称或 id

`-i` 和 `-n` 必填其中一个

`-o`：即 output，指定输出的 markdown 文件路径，必填

`-c`：即 count，如果是根据名称搜索，该字段指定搜索豆瓣的前 count 条结果，默认为 1，选填

`--id`：根据 id 进行搜索，选填

## 例子
```
# 搜索并保存白夜行在豆瓣的前2个搜索结果
BookToMarkdown.py -n 白夜行 -o output.md -c 2
```

## 豆瓣 API
```
# 根据名称搜索
DoubanBookNameApi = 'https://api.douban.com/v2/book/search?count={}&q={}'
# 根据 Id 搜索
DoubanBookIdApi = 'https://api.douban.com/v2/book/{}'
# 搜索指定用户的收藏（想看/在看/已看）
DoubanBookUserApi = 'https://api.douban.com/v2/book/user/{}/collections?count={}'
```

豆瓣更改了 API 接口，BookToMarkdown 暂时失效，得同 BookToHTML 一样，添加 apikey
