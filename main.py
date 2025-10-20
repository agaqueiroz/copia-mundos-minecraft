import platform, os, zipfile
from pathlib import Path

def identifica_windows():
    if platform.system() != "Windows":
        print("Este script só pode ser executado no Windows.")
        exit(1)
    else:
        print("Sistema operacional é Windows.")

def procura_pasta_minecraft():
    root = os.environ.get('LOCALAPPDATA')
    if root is None or root == '':
        print("Pasta principal de aplicativos locais não encontrada.")
        exit(2)
    part = '\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds'
    path = Path(root + part)
    path_list = []
    exist_worlds = False
    for i in path.iterdir():
        if i.is_dir():
            path_list.append(str(i))
            exist_worlds = True
    if not exist_worlds:
        print("Nenhum mundo do Minecraft encontrado.")
        exit(3)
    else:
        print("Possíveis mundos do Minecraft:")
        for p in path_list:
            with open(p + '\\levelname.txt', 'r') as f:
                level_name = f.read().strip()
                print('-> ' + level_name)

def cria_zip_de_mundos():
    download_path = str(Path.home() / "Downloads" / "MinecraftWorldsBackup.zip")    
    try:
        with zipfile.ZipFile(download_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            root = os.environ.get('LOCALAPPDATA')
            part = '\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds'
            if root is None or root == '':
                print("Pasta principal de aplicativos locais não encontrada.")
                exit(2)
            path = Path(root + part)
            for i in path.iterdir():
                if i.is_dir():
                    for foldername, subfolders, filenames in os.walk(i):
                        # adicionar entrada da pasta (mesmo que vazia)
                        rel_folder = os.path.relpath(foldername, path)
                        # normalizar separadores para '/'
                        arc_folder = rel_folder.replace(os.path.sep, '/') + '/'
                        if arc_folder != './':
                            zipf.writestr(arc_folder, '')
                        # adicionar arquivos da pasta
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            arcname = os.path.relpath(file_path, path).replace(os.path.sep, '/')
                            zipf.write(file_path, arcname)
        print(f"Backup criado com sucesso em: {download_path}")
    except Exception as e:
        print(f"Erro ao criar o backup: {e}")
        exit(4)


if __name__ == "__main__":
    identifica_windows()
    procura_pasta_minecraft()
    cria_zip_de_mundos()