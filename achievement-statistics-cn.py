from bs4 import BeautifulSoup
import csv
import os

file_path = 'a.html'
result_path = '成就统计.csv'


def main():
    """
    1.read html from file_path
    2.parse html tags and generate achievement list
    3.write achievement list to result path
    :return:
    """
    html = read()
    achievement_list = process(html)
    write(achievement_list)


def read():
    html = ''
    if os.path.exists(file_path):
        file = open(file_path, encoding='utf8')
        html = file.read()
        file.close()
    return html


def write(achievement_list):
    if os.path.exists(result_path):
        os.remove(result_path)
    with open(result_path, 'a', encoding='gb18030', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['成就名', '成就详情', '是否解锁', '解锁时间', '进度'])
        for item in achievement_list:
            writer.writerow(item)
        f.close()


def process(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    achievements = soup.findAll(attrs={'class': 'achieveTxt'})
    achievement_list = []
    for achievement in achievements:
        item = []
        # achievement name
        name = achievement.h3.get_text().strip()
        item.append(name)
        # achievement detail
        detail = achievement.h5.get_text().strip()
        item.append(detail)
        # achievement unlock time
        unlock_time_tag = achievement.find(attrs={'class': 'achieveUnlockTime'})
        if unlock_time_tag is not None:
            unlock_time = unlock_time_tag.get_text().replace('<br>', '').strip()
            item.append('是')
            item.append(unlock_time)
        else:
            item.append('否')
            item.append(' ')
        # achievement process
        process_tag = achievement.find(attrs={'class': 'progressText nextToBar ellipsis'})
        if process_tag is not None:
            process_value = process_tag.get_text().strip()
            item.append(process_value)
        else:
            item.append(' ')
        # add item to list
        achievement_list.append(item)
    return achievement_list


if __name__ == '__main__':
    main()
