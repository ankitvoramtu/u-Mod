# /u/Mod
Predicting user response for automatic comment moderation.

#



#Repo Organization
```
.
├── app [Flask App]
│   ├── modU
│   │   ├── ComplexRadar.py [PolarPlot Class]
│   │   ├── config.py [Config Data]
│   │   ├── __init__.py
│   │   ├── static
│   │   ├── templates
│   │   │   ├── index.html
│   │   │   └── report.html
│   │   └── views.py
│   ├── run.py
│   └── tmp
├── data
│   ├── full_set
│   │   ├── comments [all comments reddit 2015]
│   │   └── posts [all posts reddit 2015]
│   ├── political_data [Political subs]
│   │   ├── full_year [political subs for the year]
│   │   │   ├── political_comments.json
│   │   │   └── political_posts.json
│   │   ├── PoliticalSubs.txt [A list of political subs]
│   │   ├── subset_subreddits.py[How I subset the complete set of subs.]
│   │   └── three_month [political subs for 01-02]
│   │       ├── 01-02_political_comments.json
│   │       └── 01-02_political_posts.json
│   └── reddit_data
│       └── known_bots.json [A list of previously known bots]
├── README.md
└── setup
    ├── build_models.py
    ├── config.py
    ├── create_db.py
    ├── DataExploration.ipynb
    ├── insert_file.py
    ├── liwk.json
    ├── liwk.py
    ├── README.md
    ├── string_cleaning.py
    └── test.pickle
```
