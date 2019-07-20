rm -rf ~/Tempo build dist

RED='\x1B[0;31m'
NC='\x1B[0m'

echo -e "${RED}0. Probably need a new version?${NC}"
python src/upload.py

echo -e "${RED}1. run pyinstaller - this takes 15 seconds...${NC}"
cp app/pyinstaller.spec .
pyinstaller --onefile --windowed --osx-bundle-identifier com.chrislaffra.osx.tempo pyinstaller.spec 2>&1 | grep ERROR
rm pyinstaller.spec

rm -rf build
echo -e "${RED}2. cp -R tempo.app dist${NC}"
cp -R app/tempo.app.template dist/tempo.app
echo -e "${RED}3. mv dist/tempo dist/tempo.app/Contents/MacOS${NC}"
mv dist/tempo dist/tempo.app/Contents/MacOS

echo -e "${RED}4. code sign package${NC}"
codesign -v -f --deep -i com.chrislaffra.osx.tempo -s "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" dist/tempo.app/Contents/MacOs/tempo
codesign -v -f -i com.chrislaffra.osx.tempo -s "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" dist/tempo.app

cd dist
echo -e "${RED}5. create-dmg Tempo.app${NC}"
create-dmg Tempo.app
mv tempo\ 0.1.0.dmg tempo.dmg
cd ..

echo -e "${RED}6. code sign dmg${NC}"
codesign -v -f -i com.chrislaffra.osx.tempo -s "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" dist/tempo.dmg
ls -l dist

echo -e "${RED}7. done building${NC}"
echo -e "${RED}8. Final step: open dist/tempo.dmg"
open dist/tempo.dmg
