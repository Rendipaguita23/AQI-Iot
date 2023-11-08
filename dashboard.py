import streamlit as st
import paho.mqtt.client as mqtt
from datetime import datetime
import plotly.graph_objs as go
from PIL import Image

image = Image.open('AQI.png')
st.image(image, width=700)

# Inisialisasi aplikasi Streamlit
st.markdown("<center><h1>Air Quality Monitoring Berbasis Iot</h1></center>", unsafe_allow_html=True)
st.markdown("<center><h2>PLTU Banten 3 Lontar</h2></center>", unsafe_allow_html=True)

# Variabel-variabel koneksi MQTT
broker = "test.mosquitto.org"
port = 1883
topic_temp = "lontar/temp"
topic_humd = "lontar/humd"
topic_co = "lontar/co"
topic_so2 = "lontar/so2" 
topic_no2 = "lontar/no2"
topic_pm1 = "lontar/pm1"
topic_pm25 = "lontar/pm25"
topic_pm10 = "lontar/pm10"
mqtt_connected = False  # Variabel status koneksi MQTT

# Buat wadah kosong untuk output nilai dan grafik
output_container1 = st.empty()
chart_container1 = st.empty()

output_container2 = st.empty()
chart_container2 = st.empty()

output_container3 = st.empty()
chart_container3 = st.empty()

output_container4 = st.empty()
chart_container4 = st.empty()

output_container5 = st.empty()
chart_container5 = st.empty()

output_container6 = st.empty()
chart_container6 = st.empty()

output_container7 = st.empty()
chart_container7 = st.empty()

output_container8 = st.empty()
chart_container8 = st.empty()

# Variabel-variabel grafik garis
data1 = []  # Simpan data dari topik pertama dalam list
data2 = []  # Simpan data dari topik kedua dalam list
data3 = []  # Simpan data dari topik pertama dalam list
data4 = []  # Simpan data dari topik kedua dalam list
data5 = []  # Simpan data dari topik pertama dalam list
data6 = []  # Simpan data dari topik kedua dalam list
data7 = []  # Simpan data dari topik pertama dalam list
data8 = []  # Simpan data dari topik kedua dalam list
max_data_points = 1440  # Batasi jumlah data yang ditampilkan pada grafik (1 hari x 60 menit)

# Fungsi yang akan dipanggil saat koneksi MQTT berhasil
def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    mqtt_connected = True
    client.subscribe(topic_temp)  # Langganan ke topik MQTT pertama setelah koneksi berhasil
    client.subscribe(topic_humd)  # Langganan ke topik MQTT kedua setelah koneksi berhasil
    client.subscribe(topic_co)  # Langganan ke topik MQTT pertama setelah koneksi berhasil
    client.subscribe(topic_so2)  # Langganan ke topik MQTT kedua setelah koneksi berhasil
    client.subscribe(topic_no2)  # Langganan ke topik MQTT pertama setelah koneksi berhasil
    client.subscribe(topic_pm1)  # Langganan ke topik MQTT kedua setelah koneksi berhasil
    client.subscribe(topic_pm25)  # Langganan ke topik MQTT kedua setelah koneksi berhasil
    client.subscribe(topic_pm10)  # Langganan ke topik MQTT kedua setelah koneksi berhasil

# Fungsi yang akan dipanggil saat pesan MQTT diterima
def on_message(client, userdata, msg):
    try:
        sensor_data = msg.payload.decode("utf-8")  # Parsing pesan MQTT
        if msg.topic == topic_temp:
            update_output(output_container1, sensor_data, "°C", "Suhu")  # Perbarui output nilai untuk topik pertama
            update_line_chart(chart_container1, data1, sensor_data)  # Perbarui grafik garis untuk topik pertama
        elif msg.topic == topic_humd:
            update_output(output_container2, sensor_data, "%", "Humadity")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container2, data2, sensor_data)  # Perbarui grafik garis untuk topik kedua
        elif msg.topic == topic_co:
            update_output(output_container3, sensor_data, "PPB", "CO")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container3, data3, sensor_data)  # Perbarui grafik garis untuk topik kedua
        elif msg.topic == topic_so2:
            update_output(output_container4, sensor_data, "PPB", "SO2")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container4, data4, sensor_data)  # Perbarui grafik garis untuk topik kedua
        elif msg.topic == topic_no2:
            update_output(output_container5, sensor_data, "PPB", "NO2")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container5, data5, sensor_data)  # Perbarui grafik garis untuk topik kedua
        elif msg.topic == topic_pm1:
            update_output(output_container6, sensor_data, "µm/m3", "PM1")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container6, data6, sensor_data)  # Perbarui grafik garis untuk topik kedua
        elif msg.topic == topic_pm25:
            update_output(output_container7, sensor_data, "µm/m3", "PM2.5")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container7, data7, sensor_data)  # Perbarui grafik garis untuk topik kedua
        elif msg.topic == topic_pm10:
            update_output(output_container8, sensor_data, "µm/m3", "PM10")  # Perbarui output nilai untuk topik kedua
            update_line_chart(chart_container8, data8, sensor_data)  # Perbarui grafik garis untuk topik kedua

    except Exception as e:
        st.error(f"Error parsing MQTT message: {e}")

# Fungsi untuk memperbarui output nilai
def update_output(output_container, sensor_data, unit, topic_label):
    output_container.metric(topic_label, f"{sensor_data} {unit}")

# Fungsi untuk memperbarui data pada grafik garis
def update_line_chart(chart_container, data, sensor_data):
    current_time = datetime.now().strftime("%H:%M:%S")
    data.append((current_time, sensor_data))
    
    # Proses data waktu untuk sumbu x
    x_time = [entry[0] for entry in data]
    # Ambil data sensor untuk sumbu y
    y_sensor = [entry[1] for entry in data]
    # Tampilkan grafik garis menggunakan Plotly dalam wadah yang sudah dibuat
    fig = go.Figure(data=go.Scatter(x=x_time, y=y_sensor, mode='lines'))
    chart_container.plotly_chart(fig, use_container_width=True, key='line_chart')

    if len(data) > max_data_points:
        data.pop(0)

# Koneksi awal ke broker MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_forever()

