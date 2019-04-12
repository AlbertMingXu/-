#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import asyncio
import random
import pandas as pd
from pyppeteer import launch
from pyppeteer.element_handle import ElementHandle


def input_time_random():
    return random.randint(100, 151)


async def get_text_content(obj, path, property_name='textContent'):
    if isinstance(obj, ElementHandle) is True:
        items = await obj.xpath(path)
        values = list()
        for item in items:
            content = await (await item.getProperty(property_name)).jsonValue()
            values.append(content.strip())

        return [None, ] if not values else values


async def get_douban_comment(page):
    """
    获取豆瓣评论信息，以数组形式返回当前页面所有评论信息
    :param page: browser.newPage()
    :return: [['评论人', '观影状态', '评分', '投票数', '评论时间', '评论内容'], ]
    """
    info = list()
    comment_items = await page.xpath(
        "/html/body/div[@id='wrapper']/div[@id='content']//div[@class='article']/div[@id='comments']/div[@class='comment-item']//div[@class='comment']")

    for comment_item in comment_items:
        comment_votes = (await get_text_content(comment_item, "./h3/span[@class='comment-vote']/span[@class='votes']"))[
            0]

        commentator = (await get_text_content(comment_item, "./h3/span[@class='comment-info']/a"))[0]
        comment_span = (await get_text_content(comment_item, "./h3/span[@class='comment-info']/span[1]"))[0]
        comment_rating = (
            await get_text_content(comment_item, "./h3/span[@class='comment-info']/span[contains(@class, 'allstar')]",
                                   'title'))[0]
        comment_time = \
            (await get_text_content(comment_item, "./h3/span[@class='comment-info']/span[@class='comment-time ']"))[0]

        comment_short = (await get_text_content(comment_item, "./p/span[@class='short']"))[0]

        info.append(
            [commentator, comment_span, comment_rating, comment_votes, comment_time, comment_short])

    return info


async def login_douban(page, username, password):
    await page.goto('https://www.douban.com/')
    await page.waitFor("#anony-reg-new > div")
    await page.evaluate('''() =>{Object.defineProperties(navigator,{webdriver:{get: () => false}})}''')

    iframe_login = page.frames[1]

    await iframe_login.click(
        'body > div.account-body.login-wrap.login-start.account-anonymous > div.account-body-tabs > ul.tab-start > li.account-tab-account')
    page.mouse
    time.sleep(1)
    # 输入用户名，密码
    await iframe_login.type('#username', username, {'delay': input_time_random() - 50})  # delay是限制输入的时间
    await iframe_login.type('#password', password, {'delay': input_time_random() - 50})
    await iframe_login.click(
        'body > div.account-body.login-wrap.login-start.account-anonymous > div.account-tabcon-start > div.account-form > div.account-form-field-submit > a')
    page.mouse
    await page.waitFor(20)
    await page.waitForNavigation()


async def main(url, username, password):
    browser = await launch({'headless': False})
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(0)
    await page.setViewport({"width": 1900, "height": 1100})
    await login_douban(page, username, password)

    time.sleep(1)
    await page.goto(url)
    # content = await page.content()
    # cookies = await page.cookies()

    comments_list = list()

    while True:
        comment = await get_douban_comment(page)
        comments_list = comments_list + comment

        try:
            await page.click('#paginator > a.next')
        except:
            break

        time.sleep(5)

    df = pd.DataFrame(comments_list, columns=['commentator', 'comment_span', 'comment_rating', 'comment_votes', 'comment_time', 'comment_short'])
    df.to_excel('/Users/albert.ming.xu/Downloads/aquaman.xlsx')


if __name__ == '__main__':
    url, username, password = ('https://movie.douban.com/subject/3878007/comments?status=P', '18611111111', '12345678')
    asyncio.get_event_loop().run_until_complete(main(url, username, password))
