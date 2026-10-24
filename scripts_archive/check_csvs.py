import os
for f in os.listdir('.'):
    if f.endswith('.csv'):
        print(f, os.path.getsize(f), 'bytes')
