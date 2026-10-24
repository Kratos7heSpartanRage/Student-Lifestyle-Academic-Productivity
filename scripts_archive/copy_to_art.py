import shutil, os

art_dir = r'C:\Users\makku\.gemini\antigravity-ide\brain\fbd9c26b-1828-4cc4-90d7-5258171e0508\figures_eda'
os.makedirs(art_dir, exist_ok=True)

src_dir = r'\\wsl$\Ubuntu-24.04\home\mayank_kumar_388\Courses\Sem 5\Data Handling & Visualization\Course Project\figures_eda'
for f in os.listdir(src_dir):
    if f.endswith('.png'):
        shutil.copy(os.path.join(src_dir, f), os.path.join(art_dir, f))
        print('Copied', f)
print('All figures copied to artifact directory!')
