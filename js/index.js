var updatetimer;

var targetimg = {
	'-100': '',
	'0': 'image/label0.jpg',
	'1': 'image/label5.jpg',
        '2': 'image/label2.jpg',
	'3': 'image/Open.jpg',
        '4': 'image/Close.jpg',
        '5': 'image/label5.jpg'
}
var targetname = {
	'-100': '-',
	'0': 'label 0',
	'1': 'label 1',
	'2': 'ペットボトル大',
        '3': 'Open',
        '4': 'Close',
        '5': 'ペットボトル',
}

// 設定画面へ遷移
function open_setting() {
	var form = document.getElementById('main_form');
	form.action = '/setting.html';
	form.submit();
}

// 学習データ作成設定ダイアログ画面を開く
function open_dialog() {
	document.getElementById('message').innerHTML = '';
       document.getElementById('learning_error_message').innerHTML = '';
	document.getElementById('my_modal').style.display = 'block';	
}

// 学習データ作成する
function do_learning() {
	document.getElementById('message').innerHTML = '';
	document.getElementById('learning_error_message').innerHTML = '';
	var learning_time = document.getElementById('learning_time').value;
	var learning_label = document.getElementById('learning_label').value;
	if (learning_time == (null || '')) {
		document.getElementById('learning_error_message').innerHTML = '・測定時間[s]の値を入力してください。';
		return;
	}
	if (learning_label == (null || '')) {
		document.getElementById('learning_error_message').innerHTML = '・ラベルの値を入力してください。';
		return;
	}
	d3.text('/execLearning', {
		method : 'POST',
		body : 'learning_time=' + learning_time + '&learning_label=' + learning_label,
		headers : {
			'Content-type' : 'application/x-www-form-urlencoded'
		}
	}).then(function(data) {
		if (data == 'OK') {
			close_dialog();
			document.getElementById('message').innerHTML = '・学習データ作成成功しました。';
		} else {
			document.getElementById('learning_error_message').innerHTML = data;
		}
	});
}

// 学習データ作成設定ダイアログ画面を閉じる
function close_dialog() {
	document.getElementById('my_modal').style.display = 'none';
}

// モデル作成
function make_model() {
	document.getElementById('message').innerHTML = '';
	d3.text('/makeModel', {
		method : 'POST',
		body : '',
		headers : {
			'Content-type' : 'application/x-www-form-urlencoded'
		}
	}).then(function(data) {
		if (data == 'OK') {
			document.getElementById('message').innerHTML = '・モデル作成成功しました。';
		} else {
			document.getElementById('message').innerHTML = data;
		}
	});
}

// デモ実行
function exec_demo() {
	document.getElementById('message').innerHTML = '';
	d3.text('/execDemo', {
		method : 'POST',
		body : '',
		headers : {
			'Content-type' : 'application/x-www-form-urlencoded'
		}
	}).then(function(data) {
		if (data == 'OK') {
			get_update_data();
		} else {
			document.getElementById('message').innerHTML = data;
		}
	});
}

function get_update_data() {
	d3.json('/updateData', {
		method : 'POST',
		body : '',
		headers : {
			'Content-type' : 'application/x-www-form-urlencoded'
		}
	}).then(function(data) {
		result = data['result'];
		if (result == 'STOP') {
		} else if (result == 'RETRY') {
			updatetimer = setTimeout(get_update_data, 100);
		} else {
			// データ取得
			snr_data = data['snr'];
			frequency_data = data['phase'];
			result_accuracy_data = data['accuracy'];
			result_package_data = data['package'];
			target_data = data['image']
			// 解析結果更新
			var len = result_accuracy_data.length - 1;
			document.getElementById('image').src = targetimg[target_data[len].y];
			document.getElementById('name').innerHTML = targetname[target_data[len].y];
			document.getElementById('accuracy').innerHTML = result_accuracy_data[len].y;
			document.getElementById('package').innerHTML = result_package_data[len].y;
			// グラフ更新
			snrchart.update();
			frequencychart.update();
			resultchart.update();
			updatetimer = setTimeout(exec_demo, 1000);
		}
	});
}

var snrchart;
var frequencychart;
var resultchart;
// 初期化
function on_load() {
	snrchart = new snr_chart();
	frequencychart = new frequency_chart();
	resultchart = new result_chart();
	d3.json('/initIndex', {
		method : 'POST',
		headers : {
			'Content-type' : 'application/x-www-form-urlencoded'
		}
	}).then(function(data) {
		console.log(data);
	});
}

// SNRグラフ
var snr_data = [];
var snr_chart = function() {
	self = this;
	// 前回のグラフを削除する
	this.div = d3.select('#chart-snr');
	this.div.selectAll('svg').remove();
	// SNRフラグ対象を取得する
	this.chart = this.div.append('svg').attr('width', 1800).attr('height', 480).append('g').attr('transform', 'translate(180, 90)');
	// タイトルを描画する
	this.chart.append('g').append('text').attr('fill', 'black').attr('x', 0).attr('y', -50).attr('text-anchor', 'middle').attr('font-size', '30pt')
			.attr('font-weight', 'bold').text('SNR');
	// X軸を描画する
	this.x = d3.scaleLinear().domain([ 1, 10 ]).range([ 0, 1300 ]);
	this.xAxis = d3.axisBottom().scale(this.x);
	this.axisX = this.chart.append('g').attr('class', 'x axis').attr('transform', 'translate(0, 350)').call(this.xAxis);
	this.axisX.append('text').attr('fill', 'black').attr('x', 1400).attr('y', 10).attr('text-anchor', 'middle').attr('font-size', '30pt').attr(
			'font-weight', 'bold').text('time');
	// Y軸を描画する
	this.y = d3.scaleLinear().domain([ 20, 40 ]).range([ 350, 0 ]);
	this.yAxis = d3.axisLeft().scale(this.y);
	this.axisY = this.chart.append('g').attr('class', 'y axis').call(this.yAxis);
	this.axisY.append('text').attr('fill', 'black').attr('x', -200).attr('y', -90).attr('text-anchor', 'middle').attr('transform', 'rotate(-90)')
			.attr('font-size', '30pt').attr('font-weight', 'bold').text('SNR[dB]');
	// 線を描画する
	this.line = d3.line().x(function(d) {
		return self.x(d.x);
	}).y(function(d) {
		return self.y(d.y);
	});
	// 描画エリアを設定する
	this.chipPath = this.chart.append('clipPath').attr('id', 'clip-rect').append('rect').attr('width', 1300).attr('height', 350);
	this.path = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
}

// SNRグラフのリアルタイム更新
snr_chart.prototype.update = function() {
	self = this;
	var xmin = 1;
	var xmax = 10;
	var ymin = 0;
	var ymax = 100;
	for (var i = 0; i < snr_data.length; i++) {
		xmin = Math.max(this.x.domain()[0], snr_data[i].x);
		xmax = Math.max(this.x.domain()[1], snr_data[i].x);
		ymin = Math.min(this.y.domain()[0], snr_data[i].y);
		ymax = Math.max(this.y.domain()[1], snr_data[i].y);
	}
	if (xmax - xmin < 9) {
		xmin = xmax - 9;
	} 
	this.x.domain([ xmin, xmax ]);
	this.path.datum(snr_data).attr('class', 'smoothline').attr('d', self.line);
	this.axisX.call(this.xAxis);
	this.y.domain([ ymin, ymax ]);
	this.axisY.call(this.yAxis);
}

// 周波数グラフ
var frequency_data = [];
var frequency_chart = function() {
	self = this;
	// 前回のグラフを削除する
	this.div = d3.select('#chart-frequency');
	this.div.selectAll('svg').remove();
	// SNRフラグ対象を取得する
	this.chart = this.div.append('svg').attr('width', 1800).attr('height', 480).append('g').attr('transform', 'translate(180, 90)');
	// タイトルを描画する
	this.chart.append('g').append('text').attr('fill', 'black').attr('x', 0).attr('y', -50).attr('text-anchor', 'middle').attr('font-size', '30pt')
			.attr('font-weight', 'bold').text('φ/ψ');
	// X軸を描画する
	this.x = d3.scaleLinear().domain([ 1, 52 ]).range([ 0, 1300 ]);
	this.xAxis = d3.axisBottom().scale(this.x);
	this.axisX = this.chart.append('g').attr('class', 'x axis').attr('transform', 'translate(0, 350)').call(this.xAxis);
	this.axisX.append('text').attr('fill', 'black').attr('x', 1460).attr('y', 10).attr('text-anchor', 'middle').attr('font-size', '30pt').attr(
			'font-weight', 'bold').text('frequency');
	// Y軸を描画する
	this.y = d3.scaleLinear().domain([ 0, 6.5 ]).range([ 350, 0 ]);
	this.yAxis = d3.axisLeft().scale(this.y);
	this.axisY = this.chart.append('g').attr('class', 'y axis').call(this.yAxis);
	this.axisY.append('text').attr('fill', 'black').attr('x', -200).attr('y', -90).attr('text-anchor', 'middle').attr('transform', 'rotate(-90)')
			.attr('font-size', '30pt').attr('font-weight', 'bold').text('angle[rad]');
	// 線を描画する
	this.line = d3.line().curve(d3.curveCardinal).x(function(d) {
		return self.x(d.x);
	}).y(function(d) {
		return self.y(d.y);
	});
	// 描画エリアを設定する
	this.chipPath = this.chart.append('clipPath').attr('id', 'clip-rect').append('rect').attr('width', 1300).attr('height', 350);
	this.path1 = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
	this.path2 = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
	this.path3 = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
	this.path4 = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
	this.path5 = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
	this.path6 = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
	// 凡例を描画する
	this.axisX.append('text').attr('fill', '#ff0000').attr('x', 1430).attr('y', -380).attr('text-anchor', 'middle').attr('font-size', '25pt').attr(
			'font-weight', 'bold').text('φ11');
	this.axisX.append('text').attr('fill', '#ff8000').attr('x', 1430).attr('y', -340).attr('text-anchor', 'middle').attr('font-size', '25pt').attr(
			'font-weight', 'bold').text('φ21');
	this.axisX.append('text').attr('fill', '#008000').attr('x', 1430).attr('y', -300).attr('text-anchor', 'middle').attr('font-size', '25pt').attr(
			'font-weight', 'bold').text('φ31');
	this.axisX.append('text').attr('fill', '#0000ff').attr('x', 1430).attr('y', -260).attr('text-anchor', 'middle').attr('font-size', '25pt').attr(
			'font-weight', 'bold').text('ψ21');
	this.axisX.append('text').attr('fill', '#80ffff').attr('x', 1430).attr('y', -220).attr('text-anchor', 'middle').attr('font-size', '25pt').attr(
			'font-weight', 'bold').text('ψ31');
	this.axisX.append('text').attr('fill', '#c0c0c0').attr('x', 1430).attr('y', -180).attr('text-anchor', 'middle').attr('font-size', '25pt').attr(
			'font-weight', 'bold').text('ψ41');
}

// 周波数グラフのリアルタイム更新
frequency_chart.prototype.update = function() {
	self = this;
	var ymin = 0;
	var ymax = 2;
	for (var i = 0; i < frequency_data.length; i++) {
		for (var j = 0; j < frequency_data[i].length; j++) {
			ynew = parseInt(frequency_data[i][j].y) + 1 
			ymin = Math.min(this.y.domain()[0], ynew);
			ymax = Math.max(this.y.domain()[1], ynew);
		}
	}
	this.y.domain([ ymin, ymax ]);
	this.axisY.call(this.yAxis);
	this.path1.datum(frequency_data[0]).attr('class', 'smoothline1').attr('d', self.line);
	this.path2.datum(frequency_data[1]).attr('class', 'smoothline2').attr('d', self.line);
	this.path3.datum(frequency_data[2]).attr('class', 'smoothline3').attr('d', self.line);
	this.path4.datum(frequency_data[3]).attr('class', 'smoothline4').attr('d', self.line);
	this.path5.datum(frequency_data[4]).attr('class', 'smoothline5').attr('d', self.line);
	this.path6.datum(frequency_data[5]).attr('class', 'smoothline6').attr('d', self.line);
}

// 解析結果グラフ
var result_accuracy_data = [];
var result_package_data = [];
var result_chart = function() {
	self = this;
	// 前回のグラフを削除する
	this.div = d3.select('#chart-result');
	this.div.selectAll('svg').remove();
	// SNRフラグ対象を取得する
	this.chart = this.div.append('svg').attr('width', 1800).attr('height', 480).append('g').attr('transform', 'translate(180, 90)');
	// タイトルを描画する
	this.chart.append('g').append('text').attr('fill', 'black').attr('x', 0).attr('y', -50).attr('text-anchor', 'middle').attr('font-size', '30pt')
			.attr('font-weight', 'bold').text('解析結果');
	// X軸を描画する
	this.x = d3.scaleLinear().domain([ 1, 10 ]).range([ 0, 1300 ]);
	this.xAxis = d3.axisBottom().scale(this.x);
	this.axisX = this.chart.append('g').attr('class', 'x axis').attr('transform', 'translate(0, 350)').call(this.xAxis);
	this.axisX.append('text').attr('fill', 'black').attr('x', 1400).attr('y', 10).attr('text-anchor', 'middle').attr('font-size', '30pt').attr(
			'font-weight', 'bold').text('time');
	// Y軸を描画する
	this.y = d3.scaleLinear().domain([ 0, 100 ]).range([ 350, 0 ]);
	this.yAxis = d3.axisLeft().scale(this.y);
	this.axisY = this.chart.append('g').attr('class', 'y axis').call(this.yAxis);
	this.axisY.append('text').attr('fill', 'black').attr('x', -200).attr('y', -90).attr('text-anchor', 'middle').attr('transform', 'rotate(-90)')
			.attr('font-size', '30pt').attr('font-weight', 'bold').text('精度[%]');
	this.axisY.append('text').attr('fill', 'black').attr('x', 140).attr('y', -1360).attr('text-anchor', 'middle').attr('transform', 'rotate(90)').attr(
			'font-size', '25pt').attr('font-weight', 'bold').text('取得パケット数[個]');
	// 線を描画する
	this.line = d3.line().x(function(d) {
		return self.x(d.x);
	}).y(function(d) {
		return self.y(d.y);
	});
	// 描画エリアを設定する
	this.chipPath = this.chart.append('clipPath').attr('id', 'clip-rect').append('rect').attr('width', 1300).attr('height', 350);
	this.path = this.chart.append('path').attr('clip-path', 'url(#clip-rect)');
}

// 解析結果グラフのリアルタイム更新
result_chart.prototype.update = function() {
	self = this;
	var xmin = 1;
	var xmax = 10;
	var ymin = 0;
	var ymax = 100;
	for (var i = 0; i < result_accuracy_data.length; i++) {
		xmin = Math.max(this.x.domain()[0], result_accuracy_data[i].x);
		xmax = Math.max(this.x.domain()[1], result_accuracy_data[i].x);
		ymin = Math.min(this.y.domain()[0], result_accuracy_data[i].y);
		ymax = Math.max(this.y.domain()[1], result_accuracy_data[i].y);
	}
	if (xmax - xmin < 9) {
		xmin = xmax - 9;
	} 
	this.x.domain([ xmin, xmax ]);
	this.path.datum(result_accuracy_data).attr('class', 'smoothline').attr('d', self.line);
	this.axisX.call(this.xAxis);
	this.y.domain([ ymin, ymax ]);
	this.axisY.call(this.yAxis);
	// 点を描画する
	this.chart.selectAll('.dot').remove();
	this.chart.selectAll('.dot').data(result_accuracy_data).enter().append('circle').attr('class', 'dot').attr('cx', function(d, i) {
		return self.x(d.x)
	}).attr('cy', function(d) {
		return self.y(d.y)
	}).attr('r', 8);
	// 取得パケット数を描画する
	this.chart.selectAll('.dottext').remove();
	this.chart.selectAll('.dottext').data(result_accuracy_data).enter().append('text').attr('class', 'dottext').attr('x', function(d) {
		return self.x(d.x);
	}).attr('y', function(d) {
		return self.y(d.y);
	}).text(function(d, i) {
		return result_package_data[i].y;
	});
}
