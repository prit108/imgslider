:
echo  "Each pair of sums should match"

echo  "python tilesSearch.py 42_713856  ratio=2 time=0 | sum"
python  tilesSearch.py 42_713856  ratio=2 time=0 | sum
python3 tilesSearch.py 42_713856  ratio=2 time=0 | sum
echo
echo  "python tilesSearch.py 42_713856  ratio=0 time=0 | sum"
python  tilesSearch.py 42_713856  ratio=0 time=0 | sum
python3 tilesSearch.py 42_713856  ratio=0 time=0 | sum
echo
echo "python tilesGreedy.py 1234_5678 time=0 | sum"
python  tilesGreedy.py 1234_5678 time=0 | sum
python3 tilesGreedy.py 1234_5678 time=0 | sum
echo
