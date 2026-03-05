import os
import requests

dat_urls = [
"https://m-selig.ae.illinois.edu/ads/coord/ht05.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe443.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ht08.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ht12.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe444.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ea81006.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca0006.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca16006.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s1010.dat",
"https://m-selig.ae.illinois.edu/ads/coord/m1.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe445.dat",
"https://m-selig.ae.illinois.edu/ads/coord/hq07.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s9033.dat",
"https://m-selig.ae.illinois.edu/ads/coord/raf30md.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca000834.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx77080.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s9027.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca0008.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n64008a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/m2.dat",
"https://m-selig.ae.illinois.edu/ads/coord/hq09.dat",
"https://m-selig.ae.illinois.edu/ads/coord/nacam2.dat",
"https://m-selig.ae.illinois.edu/ads/coord/lwk80080.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx71089a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n0009sm.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ea61009.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ys900.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca16009.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s9032.dat",
"https://m-selig.ae.illinois.edu/ads/coord/eh0009.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s9026.dat",
"https://m-selig.ae.illinois.edu/ads/coord/b540ols.dat",
"https://m-selig.ae.illinois.edu/ads/coord/raf27.dat",
"https://m-selig.ae.illinois.edu/ads/coord/bqm34.dat",
"https://m-selig.ae.illinois.edu/ads/coord/sc20010.dat",
"https://m-selig.ae.illinois.edu/ads/coord/rae104.dat",
"https://m-selig.ae.illinois.edu/ads/coord/rae103.dat",
"https://m-selig.ae.illinois.edu/ads/coord/rae102.dat",
"https://m-selig.ae.illinois.edu/ads/coord/rae101.dat",
"https://m-selig.ae.illinois.edu/ads/coord/rae100.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001064.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001035.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca0010.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001066.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n63010a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca64a010.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001034.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001065.dat",
"https://m-selig.ae.illinois.edu/ads/coord/lwk79100.dat",
"https://m-selig.ae.illinois.edu/ads/coord/hq010.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e230.dat",
"https://m-selig.ae.illinois.edu/ads/coord/sd8020.dat",
"https://m-selig.ae.illinois.edu/ads/coord/lwk80100.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx79l100.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx76100.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n0011sc.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e297.dat",
"https://m-selig.ae.illinois.edu/ads/coord/joukowsk.dat",
"https://m-selig.ae.illinois.edu/ads/coord/m3.dat",
"https://m-selig.ae.illinois.edu/ads/coord/nacam3.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n63012a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n64012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx71120.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001234.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca001264.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n64012a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/sc20012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/j5012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s1012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n0012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca16012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ea61012.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx79l120.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ah85l120.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx76120.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e472.dat",
"https://m-selig.ae.illinois.edu/ads/coord/lwk80120k25.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e171.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e168.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e836.dat",
"https://m-selig.ae.illinois.edu/ads/coord/raf30.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe409.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe459.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ultimate.dat",
"https://m-selig.ae.illinois.edu/ads/coord/ls013.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe411.dat",
"https://m-selig.ae.illinois.edu/ads/coord/stcyr172.dat",
"https://m-selig.ae.illinois.edu/ads/coord/oaf139.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e521.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s8035.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s1048.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e474.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fxl142k.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e169.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca16015.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e520.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e475.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca0015.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx711520.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx711525.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx711530.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n64015.dat",
"https://m-selig.ae.illinois.edu/ads/coord/lwk80150k25.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fx71l150.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n63015a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/n64015a.dat",
"https://m-selig.ae.illinois.edu/ads/coord/fxlv152.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e837.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe410.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e473.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s1014.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e479.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s1046.dat",
"https://m-selig.ae.illinois.edu/ads/coord/s1016.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca16018.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca633018.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca66-018.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca0018.dat",
"https://m-selig.ae.illinois.edu/ads/coord/e838.dat",
"https://m-selig.ae.illinois.edu/ads/coord/us1000root.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe460.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca16021.dat",
"https://m-selig.ae.illinois.edu/ads/coord/naca0021.dat",
"https://m-selig.ae.illinois.edu/ads/coord/goe775.dat"
]


'''
#this downloads a dat file for each profile in the list above and saves them to the download directory
#please be aware that not all foils from airfoiltools are closed curves, so either sort them out or do a spline interpolation

DOWNLOAD_DIR = "../foils_to_consider"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# === Ensure download directory exists ===
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === Download each file ===
for url in dat_urls:
    try:
        filename = url.split('/')[-1]
        file_path = os.path.join(DOWNLOAD_DIR, filename)

        print(f"Downloading {filename} → {file_path}")
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        with open(file_path, "w") as f:
            f.write(response.text)

    except Exception as e:
        print(f"Error downloading {url}: {e}")
'''


