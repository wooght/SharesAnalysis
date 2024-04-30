var test_data = ''
;xh5_define("datas.k", ["utils.util"], function(e) {
    "use strict";
    var t = e.load
    ,s = e.xh5_S_KLC_D;
    return new function() {
        // var test_data = t('https://finance.sina.com.cn/realstock/company/sz002594/hisdata_klc2/klc_kl.js?d=2024_4_29')
        test_data = s("{compress}")
        //alert("输出:"+test_data.length)
    }
})
getformartdate = function(date){
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = (date.getDate().toString().padStart(2, '0'))
    return `${year}-${month}-${day}`
}
result_list = []
test_data.forEach(function(value,index,array){
    result_list.push({'amount':value.amount,'open':value.open,'close':value.close,'low':value.low,'high':value.high,'volume':value.volume,'date':getformartdate(value.date)})
})
return result_list