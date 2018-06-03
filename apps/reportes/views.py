from django.shortcuts import render
from django.shortcuts import render_to_response
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Create your views here.

def Prueba(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")

    driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                               '--web-security=false'])
    driver.set_window_size(1024, 768)
    try:
        driver.get('http://127.0.0.1:8000/indicadores/graficos/65')
        time.sleep(2)
        driver.execute_script('document.getElementsByClassName("mp")[0].style.background = "white"')
        # driver.execute_script('document.body.style.background = "black"')
    except Exception, e:
        driver.save_screenshot('./static/graficos/testing1.png')
        driver.quit()

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('testchart.html', data)
