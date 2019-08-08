import urllib.request as request
import urllib.parse as parse
import json

class weather():
    def __init__(self):
        self.cwbUrlHead = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/'
        self.dataType_weather = 'F-C0032-001'
        self.dataType_warning = 'W-C0033-001'
        self.dataType_uv = 'O-A0005-001'
        self.dataType_eq = 'E-A0015-001'
        self.authKey = 'CWB-7DA0B64D-CBF5-4E39-84F7-B2BBF3CC75A0'
        self.locList = ['宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市', '基隆市',
                        '新竹縣', '新竹市', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '嘉義市', '屏東縣']

        self.stationCode = [['467080'], ['466990'], ['467660', '467610'], ['467350'], ['467110'], ['467990'], ['466920', '466910'], ['466880', '466900'], ['C0C480', '467050'],
                            ['467490', '467770'], ['467410', 'C0X250'], ['467440'], ['466940'], ['467570', '467571'], ['467570', '467571'], ['C0E750'], ['A0G720'], ['C0I460'],
                            ['C0K400'], ['C0M650'], ['467480'], ['C0R170', '467590']]

        self.stationName = [['宜蘭'], ['花蓮'], ['臺東', '成功'], ['澎湖'], ['金門'], ['馬祖'], ['臺北', '鞍部'], ['板橋', '淡水'], ['桃園', '新屋'], ['臺中', '梧棲'],
                            ['臺南', '新營'], ['高雄'], ['基隆'], ['新竹'], ['新竹'], ['苗栗'], ['彰師大'], ['南投'], ['斗六'], ['朴子'], ['嘉義'], ['屏東', '恆春']]

        self.locStations = dict(zip(self.locList, self.stationCode))
        self.stations = dict(zip(sum(self.stationCode, []), sum(self.stationName, [])))


    def get_weather(self, loc):
        loc = self.change_tai(loc)
        if (loc not in self.locList):
            return None
        else:
            
            weather = self.weather_crawler(loc)
            warning = self.warning_crawler(loc)
            uvIndex = self.uvIndex_crawler(loc)
            return {'weather': weather, 'warning': warning, 'uvIndex': uvIndex}


    def get_earthquake(self):
        cwb_url_eq = self.cwbUrlHead + self.dataType_eq + '?Authorization=' + self.authKey
        cwbData_eq = self.read_url(cwb_url_eq)
        eqData = cwbData_eq['records']['earthquake']
        earthquakes = []
        
        for eq in eqData:
            earthquakes.append(eq['reportImageURI'])
        return earthquakes


    def weather_crawler(self, loc):
        cwb_url_weather = self.cwbUrlHead + self.dataType_weather + '?locationName=' + parse.quote(loc) + '&Authorization=' + self.authKey
        cwbData_weather = self.read_url(cwb_url_weather)
        weatherData = cwbData_weather['records']['location'][0]['weatherElement']

        nowWeather = list([weatherData[0]['time'][0]['startTime']])
        nextWeather = list([weatherData[0]['time'][1]['startTime']])

        for weatherInfo in weatherData:
            nowWeather.append(weatherInfo['time'][0]['parameter']['parameterName'])   # in 6 hours
            nextWeather.append(weatherInfo['time'][1]['parameter']['parameterName'])  # next 12 hours

        return [nowWeather, nextWeather]    # [time, weather, rain prob., Min Temp., feel, Max Temp.]

    
    def warning_crawler(self, loc):
        cwb_url_warning = self.cwbUrlHead + self.dataType_warning + '?locationName=' + parse.quote(loc) + '&Authorization=' + self.authKey
        cwbData_warning = self.read_url(cwb_url_warning)
        Warning = cwbData_warning['records']['location'][0]['hazardConditions']['hazards']
        if(Warning != []):
            Warning = Warning[0]['info']
            weatherWarning = Warning['phenomena'] + Warning['significance']
            return weatherWarning
        else:
            return None


    def uvIndex_crawler(self, loc):
        stationCodes = ','.join(self.locStations[loc])
        staName = []
        uvIndex = []
        
        cwb_url_uv = self.cwbUrlHead + self.dataType_uv + '?locationCode=' + stationCodes + '&Authorization=' + self.authKey
        cwbData_uv = self.read_url(cwb_url_uv)
        uvData = cwbData_uv['records']['weatherElement']['location']
        uvDatatime = cwbData_uv['records']['weatherElement']['time']['dataTime']

        for uv in uvData:
            staName.append(self.stations[uv['locationCode']])
            uvIndex.append(round(uv['value']))
        return [list(zip(staName, uvIndex)), uvDatatime]


    def read_url(self, url):
        response = request.urlopen(url)
        data = response.read().decode('utf-8')
        data = json.loads(data)
        return data


    def change_tai(self, loc):
        if (loc[0] == '台'):
            loc = loc.replace('台', '臺')
        return loc


if __name__ == "__main__":
    wx = weather()
    # wx.get_weather('高雄市')
    wx.get_earthquake()
