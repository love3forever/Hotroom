# 利用mongodb3.4新特性view，创建一些耗时较长的aggregation
1. 创建所有主播列表
```
db.createView(
    'streamers',
    'Roominfo',
    [
        {
            "$group": {
                "_id": "$host",
                "catalogs": {
                    "$addToSet": "$catalog"
                },
                "count": {
                    "$sum": 1
                },
                "roomid": {
                    "$first": "$roomid"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "count": 1,
                "streamer": "$_id",
                'catalogs': "$catalogs",
                'roomid': '$roomid'
            }
        }
    ]
)
```
