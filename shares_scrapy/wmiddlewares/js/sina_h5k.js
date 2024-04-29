var test_data = ''
;xh5_define("datas.k", ["utils.util"], function(e) {
    "use strict";
    var t = e.load
    ,s = e.xh5_S_KLC_D;
    return new function() {
        // var test_data = t('https://finance.sina.com.cn/realstock/company/sz002594/hisdata_klc2/klc_kl.js?d=2024_4_29')
        test_data = s({compress})
        //alert("输出:"+test_data.length)
    }
})
return test_data