// 「確認」ボタンの処理
function save_setting() {
	var frequency = document.getElementById('frequency').value;
	var adress_ap = document.getElementById('adress_ap').value;
	var adress_sta = document.getElementById('adress_sta').value;
	var learning_file_name = document.getElementById('learning_file_name').value;
	var learning_file_output = document.getElementById('learning_file_output').value;
	var model_file_name = document.getElementById('model_file_name').value;
	var model_file_ouput = document.getElementById('model_file_ouput').value;
	var loop_time = document.getElementById('loop_time').value;
	var measurement_time = document.getElementById('measurement_time').value;
	if (frequency == (null || '')) {
		document.getElementById('error_message').innerHTML = '・周波数[MHz]の値を入力してください。';
		return;
	}
	if (adress_ap == (null || '')) {
		document.getElementById('error_message').innerHTML = '・MACアドレス（AP）の値を入力してください。';
		return;
	}
	if (adress_sta == (null || '')) {
		document.getElementById('error_message').innerHTML = '・MACアドレス（STA）の値を入力してください。';
		return;
	}
	if (learning_file_name == (null || '')) {
		document.getElementById('error_message').innerHTML = '・学習ファイル名の値を入力してください。';
		return;
	}
	if (model_file_name == (null || '')) {
		document.getElementById('error_message').innerHTML = '・モデルファイル名の値を入力してください。';
		return;
	}
	if (loop_time == (null || '')) {
		document.getElementById('error_message').innerHTML = '・ループ用クールタイム[回]の値を入力してください。';
		return;
	}
	if (measurement_time == (null || '')) {
		document.getElementById('error_message').innerHTML = '・デモ用測定時間[s]の値を入力してください。';
		return;
	}
	if (learning_file_output == (null || '')) {
		learning_file_output = '/learning';
	}
	if (model_file_ouput == (null || '')) {
		model_file_ouput = '/model';
	}
	d3.text(
			'/saveSetting',
			{
				method : 'POST',
				body : 'frequency=' + frequency + '&adress_ap=' + adress_ap + '&adress_sta=' + adress_sta + '&learning_file_name='
						+ learning_file_name + '&learning_file_output=' + learning_file_output + '&model_file_name=' + model_file_name
						+ '&model_file_ouput=' + model_file_ouput + '&loop_time=' + loop_time + '&measurement_time=' + measurement_time,
				headers : {
					'Content-type' : 'application/x-www-form-urlencoded'
				}
			}).then(function(data) {
		if (data == 'OK') {
			document.getElementById('error_message').innerHTML = '';
			do_back();
		} else {
			document.getElementById('error_message').innerHTML = data;
		}
	});
}

// 「戻る」ボタンの処理
function do_back() {
	history.back();
}

// 初期処理
function on_load() {
	d3.json('/initSetting', {
		method : 'POST',
		body : '',
		headers : {
			'Content-type' : 'application/x-www-form-urlencoded'
		}
	}).then(function(data) {
		console.log(data);
		document.getElementById('frequency').value = data['frequency'];
		document.getElementById('adress_ap').value = data['adress_ap'];
		document.getElementById('adress_sta').value = data['adress_sta'];
		document.getElementById('learning_file_name').value = data['learning_file_name'];
		document.getElementById('learning_file_output').value = data['learning_file_output'];
		document.getElementById('model_file_name').value = data['model_file_name'];
		document.getElementById('model_file_ouput').value = data['model_file_ouput'];
		document.getElementById('loop_time').value = data['loop_time'];
		document.getElementById('measurement_time').value = data['measurement_time'];
	});
}