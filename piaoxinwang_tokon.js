var puppeteer = require('puppeteer')
    const devices = require('puppeteer/DeviceDescriptors');
    const iphone = devices['iPhone 6']
    const conf = {
		executablePath: 'C:/Users/lee2fat/AppData/Local/Google/Chrome/Application/chrome.exe',
        headless: false,
        defaultViewport: {
            width: 1300,
            height:1400,
        },
        slowMo: 30
    }
    puppeteer.launch(conf).then(async browser => {
        var page = await browser.newPage()
        //await page.emulate(iphone) 
		
        await page.evaluate(async () => {
            Object.defineProperty(navigator, 'webdriver', {get: () => false})
        })
		
        await page.goto('http://vip.piaoxinwang.com/register?status=1')
        //关键点1
        await page.evaluate(async () => {
            Object.defineProperty(navigator, 'webdriver', {get: () => false})
        })
        // 输入手机号
        await page.type('input[type=text]', '19937409655', {delay: 10})
		// 输入密码
		// hxjr19937409655  |  zzf19937409655
		await page.type('input[type=password]', 'hxjr19937409655', {delay: 10})

		await page.waitFor(1000);

		//var slide_btn = await page.waitForSelector('span[id=nc_1_n1z]', {timeout: 5000})

		let  slide_btn = await page.$('span[id=nc_1_n1z]'); //有概率失败 null，奇怪
		//console.log(slide_btn)
        // 计算滑块距离
        const rect = await page.evaluate((slide_btn) => {
            const {top, left, bottom, right} = slide_btn.getBoundingClientRect();
            return {top, left, bottom, right}
        }, slide_btn)
        //console.log(rect)
        rect.left = rect.left + 10
        rect.top = rect.top + 10
        const mouse = page.mouse
        await mouse.move(rect.left, rect.top)
        // 关键点2
        await page.touchscreen.tap(rect.left, rect.top) // h5需要手动分发事件 模拟app的事件分发机制。
        await mouse.down()
        var start_time = new Date().getTime()
        await mouse.move(rect.left + 400, rect.top, {steps:27})
        await page.touchscreen.tap(rect.left + 800, rect.top,)
        //console.log(new Date().getTime() - start_time)
        await mouse.up()
		await page.waitFor(500);
        
		//console.log(await page.evaluate('navigator.webdriver'))
        //console.log('end')		
		//button

		var pass = await page.waitForSelector('span[data-nc-lang=_yesTEXT]', {timeout: 5000})



		await page.click('button')

		//获取tokon 值
		//var username= window.sessionStorage.getItem("token")

		await page.waitFor(500);
		//console.log(await page.evaluate('sessionStorage.getItem("token")'))
 		console.log(await page.evaluate('sessionStorage.getItem("sdUser")')) //获取token  {"token":"5648c10497564b86b2f00d4f154fe078","mobile":"19937409655"}

    })