cd /Users/Shared/sanskrit-lexicon/csl-orig
git show 734999be6f0477a5be315964736fe24423b7ed7d:v02/ieg/ieg.txt > temp_cdsl_ieg0.txt
mv temp_cdsl_ieg0.txt /Users/Shared/other-sanskrit-lexicon-repos/IEG/
cd /Users/Shared/other-sanskrit-lexicon-repos/IEG/issues/issue1
echo "STEP1."
python3 step1.py
echo "STEP2."
python3 step2.py
echo "STEP3."
python3 step3.py
