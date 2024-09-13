from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# Função para baixar a música em formato mp3
def baixar_musica(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        arquivo_mp3 = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    return arquivo_mp3, info_dict['title']

# Nova rota para download via GET com a URL como parâmetro
@app.route('/download', methods=['GET'])
def download_audio():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL é necessária.'}), 400

    try:
        arquivo_mp3, titulo = baixar_musica(url)
        return send_file(arquivo_mp3, as_attachment=True, download_name=f"{titulo}.mp3")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
