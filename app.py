import flet as ft
import yt_dlp
import pyperclip
import os

def main(page: ft.Page):
  
  links = []
  
  def message(success, message):
    if success:
      page.show_snack_bar(
        ft.SnackBar(
          content=ft.Text(message, color='#FFFFFF'), 
          bgcolor='#059669'  
        )
      )
    else:
      page.show_snack_bar(
        ft.SnackBar(
          content=ft.Text(message, color='#FFFFFF'), 
          bgcolor='#991b1b'  
        )
      )
    page.update()
  
  def create_folder():
    folder_path = os.path.expanduser("~/Downloads")
    folder = os.path.join(folder_path, "Mídias baixadas")
    if not os.path.exists(folder):
      os.makedirs(folder)
    return folder

  def download(url, format):    
    folder_destination = create_folder()    
    ydl_opts = {}   
    
    if format.upper() == 'MP3':
      ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(folder_destination, '%(title)s.%(ext)s'),
      }
    
    elif format.upper() == 'MP4':
      ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': os.path.join(folder_destination, '%(title)s.%(ext)s'),
      }        
           
    try:                     
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=True)        

      return True
    except Exception as e:
      return False

  def clear_links(e):
    links.clear()   
    ct_view_links.rows.clear()
    page.update()     

  def remove_link(e, index):        
    del links[index]
    update_links_view()
      
  def copy_link(e, link):
    pyperclip.copy(link)
  
  def add_link(e):    
    link_field.focus()
    if link_field.value != '' and link_field.value not in links:
      links.append(link_field.value)
      update_links_view()
      link_field.value = ''                  
      page.update()
          
  def update_links_view():
    ct_view_links.rows.clear()
    for i, link in enumerate(links):
      delete_button = ft.IconButton(
        icon=ft.icons.DELETE,
        tooltip='Remover link',
        on_click=lambda e, index=i: remove_link(e, index)
      )
      copy_button = ft.IconButton(
        icon=ft.icons.COPY,
        tooltip='Copiar link',
        on_click=lambda e, link=link: copy_link(e, link)
      )
      ct_view_links.rows.append(
          ft.DataRow(cells=[ft.DataCell(ft.Text(link)), ft.DataCell(ft.Row([delete_button, copy_button]))])
      )
    page.update()    
    
  def init_download(e):
    if not links:
      message(False, 'A lista de links está vazia!')
      return
    
    if format_file.value is None:
      message(False, 'Por favor, selecione o formato que deseja realizar o download.')
      return

    ct_view_links.rows.clear()
    total_links = len(links)
    update_progress(0, total_links)
    
    for i, link in enumerate(links, start=1):
      download(link, format_file.value)
      update_progress(i, total_links)
    
    finalize_download(total_links)
    links.clear()

  def update_progress(current, total):
    text = f"{current}/{total}"
    ct_view_links.rows.clear()
    status = 'Download em andamento...' if current < total else 'Download concluído!'
    ct_view_links.rows.append(
      ft.DataRow(cells=[ft.DataCell(ft.Text(status)), ft.DataCell(ft.Text(text))])
    )
    page.update()

  def finalize_download(total):
    ct_view_links.rows.clear()
    text = f"{total}/{total}"
    ct_view_links.rows.append(
      ft.DataRow(cells=[ft.DataCell(ft.Text('Download concluído!')), ft.DataCell(ft.Text(text))])
    )
    page.update()
                      
  # Page title
  ct_title = ft.Column(
    controls=[
      ft.Container(
        content=ft.Text('YDT', size=20, weight=ft.FontWeight.W_500),
        alignment=ft.alignment.center
      ),
      ft.Container(
        content=ft.Text('Baixe vídeos do youtube facilmente. Aproveite!', size=16, weight=ft.FontWeight.W_400),
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=30)        
      )
    ]    
  )
  
  # Field to add the video link
  link_field = ft.TextField(border_color='#EEEEEE', border_radius=15, autofocus=True, on_submit=add_link)
  add_btn = ft.FloatingActionButton(text='Adicionar link', height=49, on_click=add_link)

  ct_add_link = ft.Column(
    controls=[
      ft.Text('Link do vídeo:', weight=ft.FontWeight.W_400),
      ft.ResponsiveRow([
        ft.Container(
          link_field,
          col={"xs": 12,"sm": 12, "md": 9, "xl": 10},
        ),
        ft.Container(
          add_btn,
          col={"xs": 12,"sm": 12, "md": 3, "xl": 2},
          margin=ft.margin.only(bottom=30)
        )
      ])
    ]
  )     

  # Field to select the download format
  format_file = ft.RadioGroup(
    content=ft.Column([
      ft.Radio(value='MP3', label='MP3 - Apenas áudio'),
      ft.Radio(value='MP4', label='MP4 - Áudio e vídeo')
    ])
  )

  ct_format_file = ft.Column(
    controls=[
      ft.Text('Selecionar o formato do download:'),
      ft.Container(
        format_file,
        margin=ft.margin.only(bottom=20)
      )
    ]
  )

  # Download List
  ct_view_links = ft.DataTable(
    columns=[            
      ft.DataColumn(ft.Text('')),
      ft.DataColumn(ft.Text(''), numeric=True)
    ],
    rows=[]
  )

  # Action buttons 
  btn_init = ft.FloatingActionButton(text='Iniciar download', width=200, height=50, on_click=init_download)
  btn_clear_list = ft.FloatingActionButton(text='Limpar lista', width=200, height=50, on_click=clear_links)

  ct_btns = ft.Container(
    content=ft.ResponsiveRow([
      ft.Container(
        btn_init,
        col={"xs": 6,"sm": 6, "md": 6, "xl": 6},
        alignment=ft.alignment.center_right,
        margin=ft.margin.symmetric(vertical=60)
      ),
      ft.Container(
        btn_clear_list,
        col={"xs": 6,"sm": 6, "md": 6, "xl": 6},
        alignment=ft.alignment.center_left,
        margin=ft.margin.symmetric(vertical=60)
      )
    ]),    
  )  

  view_in_page = ft.Container(    
    padding=ft.padding.all(20),
    width=1000,
    content=ft.ResponsiveRow(
      columns=12,
      spacing=0,
      run_spacing=0,
      controls=[
        ct_title,
        ct_add_link,
        ct_format_file,
        ct_view_links,
        ct_btns
      ]
    )
  )
  
  page.title = 'YDT'
  page.scroll = ft.ScrollMode.AUTO
  page.vertical_alignament = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  

  page.add(view_in_page)
  
ft.app(target=main)
