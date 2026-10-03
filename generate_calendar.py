#!/usr/bin/env python3
import json, urllib.request, urllib.parse, hashlib
from datetime import datetime, timedelta
from pathlib import Path

YEARS = range(1405, 1412)
DATA_DIR = Path('data')
OUT = Path('calendar.ics')
BASE = 'https://raw.githubusercontent.com/alirezadesh/jalali_calendar/main/{}_data.json'

MONTHS = ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']

def esc(s):
    return str(s).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')

def fold(line, limit=73):
    # RFC 5545 line folding, kept simple for UTF-8 by folding on Python chars.
    out=[]
    while len(line) > limit:
        out.append(line[:limit])
        line=line[limit:]
    out.append(line)
    return '\r\n '.join(out)

def fetch_year(year):
    DATA_DIR.mkdir(exist_ok=True)
    p = DATA_DIR / f'{year}_data.json'
    if not p.exists():
        with urllib.request.urlopen(BASE.format(year), timeout=30) as r:
            p.write_bytes(r.read())
    return json.loads(p.read_text(encoding='utf-8'))

def wiki_url(title):
    q = urllib.parse.quote(title.replace('/', ' '), safe='')
    return f'https://fa.wikipedia.org/wiki/Special:Search?search={q}'

def main():
    events=[]
    for year in YEARS:
        days=fetch_year(year)
        for day in days:
            day_events=day.get('events') or []
            if not day_events:
                continue
            jy,jm,jd = map(int, day['date'].split('-'))
            gdate = day['date_latin'].replace('-','')
            titles=[]
            holiday=False
            for e in day_events:
                t=(e.get('description') or '').strip()
                if t and t not in titles:
                    titles.append(t)
                holiday = holiday or bool(e.get('is_holiday'))
            if not titles:
                continue
            shamsi=f'{jy:04d}/{jm:02d}/{jd:02d}'
            title=f'☀️ {shamsi} | {" / ".join(titles)}'
            desc=[f'تاریخ شمسی: {shamsi}', f'ماه: {MONTHS[jm-1]}', '', 'مناسبت‌های این روز:']
            for t in titles:
                desc.append(f'• {t}')
            if day.get('is_holiday') or holiday:
                desc += ['', 'تعطیل رسمی در تقویم داده‌شده.']
            desc += ['', 'منبع داده: jalali_calendar (داده تقویم شمسی و مناسبت‌ها)']
            uid=hashlib.sha256(f'{day["date"]}|{"|".join(titles)}'.encode('utf-8')).hexdigest()[:24]
            # All-day DTEND is exclusive. Convert using Gregorian date and datetime arithmetic.
            gd=datetime.strptime(day['date_latin'],'%Y-%m-%d').date()
            end=(gd+timedelta(days=1)).strftime('%Y%m%d')
            events.append({
                'uid': f'{uid}@iran-shamsi-calendar',
                'dtstart': gdate,
                'dtend': end,
                'summary': title,
                'description': '\n'.join(desc),
                'url': wiki_url(titles[0]),
                'holiday': holiday or bool(day.get('is_holiday')),
            })
    events.sort(key=lambda x:(x['dtstart'],x['summary']))
    now=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    lines=[
        'BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Iran Shamsi Calendar//Apple Calendar//FA','CALSCALE:GREGORIAN','METHOD:PUBLISH',
        'X-WR-CALNAME:تقویم شمسی ایران | مناسبت‌ها','X-WR-CALDESC:تقویم شمسی ایران با مناسبت‌ها و تعطیلات، قابل اشتراک در Apple Calendar','X-WR-TIMEZONE:Asia/Tehran',
    ]
    for e in events:
        lines += ['BEGIN:VEVENT',f'UID:{e["uid"]}',f'DTSTAMP:{now}',f'DTSTART;VALUE=DATE:{e["dtstart"]}',f'DTEND;VALUE=DATE:{e["dtend"]}',f'SUMMARY:{esc(e["summary"])}',f'DESCRIPTION:{esc(e["description"])}',f'URL:{e["url"]}']
        if e['holiday']:
            lines.append('CATEGORIES:تعطیل رسمی')
        else:
            lines.append('CATEGORIES:مناسبت')
        lines.append('END:VEVENT')
    lines.append('END:VCALENDAR')
    OUT.write_text('\r\n'.join(fold(x) for x in lines)+'\r\n', encoding='utf-8')
    print(f'Generated {OUT} with {len(events)} all-day events for years {min(YEARS)}-{max(YEARS)}')

if __name__=='__main__': main()
