# KrawlerPTT

KrawlerPTT is a simple crawler to obtain PTT posts. 

[中文說明](#mandarin)

## Requirement
Your device should install those package first:
* python version: 3.9+
* beautifulsoup4
* requests
* pandas
* selenium

## Usage

After downloading this repository, you can execute it in the terminal in this way:

```bash
python KrawlerPTT.py -b boardName -p NumOfPages
```

The `-b` and `-p` arguments are optional, within those arguments, you can crawl a specific board and set how many pages you want to collelect data from. 

If you don't execute this program without any argument, the deault is crawling the Gossiping borad for 1 page.

### Examples

This will crawl the Gossiping borad for 1 page:

```bash
python KrawlerPTT.py
```

This will crawl the Gossiping borad for 10 page:

```bash
python KrawlerPTT.py -p 10
```

This will crawl the WomenTalk borad for 1 page:

```bash
python KrawlerPTT.py -b WomenTalk
```
## Data we collect
* article ID
* article title
* author（username+ID）
* board
* article content
* post time
* author IP
* comments
* rating（push/boo/neutral）
* commenters
* polarity

The final data will output as "output.csv" in the current directory.

---
<a name = "mandarin"></a>
KrawlerPTT 是一個非常簡單的爬蟲小程式，可以用來爬取 PTT 的文章。

## 環境需求
您的電腦須安裝以下套件：
* python 版本 3.9或以上
* beautifulsoup4
* requests
* pandas
* selenium

## 使用方法

下載程式後，在終端機輸入以下指令執行：

```bash
python KrawlerPTT.py -b 看板名稱 -p 抓取頁數
```

參數 `-b` 和 `-p` 不是必要的，這兩個參數是用來選擇要爬取的PTT看板以及爬取頁數。如果不加的話，預設會爬取八卦板最新的一頁文章。

### 使用範例

爬取一頁八卦板文章：

```bash
python KrawlerPTT.py
```

爬取十頁八卦板文章：

```bash
python KrawlerPTT.py -p 10
```

爬取一頁女板文章：

```bash
python KrawlerPTT.py -b WomenTalk
```

## 收集資料

這個爬蟲能夠抓取特定看板的：

* 文章 ID
* 文章標題
* 文章作者（名稱+ID）
* 文章所處看板
* 文章內容
* 發文時間
* 作者IP
* 評論內容
* 評論等第（推/噓/中立）
* 評論者
* 評論等第總數（各等第的數量統計）

最終資料會在當前目錄輸出為 "output.csv"檔案。