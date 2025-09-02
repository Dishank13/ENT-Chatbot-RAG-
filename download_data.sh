#!/usr/bin/env bash
set -e

BASE_DIR="data"
mkdir -p "$BASE_DIR"

echo "1️⃣ Downloading AAO-HNSF guideline PDF..."
curl -L \
  "https://www.entnet.org/wp-content/uploads/2021/04/adult-sinusitis-physicianresource-diagnostic-criteria-rhinosinusitis.pdf" \
  -o "$BASE_DIR/AAO-HNSF_Guidelines.pdf"

echo "2️⃣ Downloading ENT surgeon patient records (CSV) from Kaggle..."
python -m kaggle datasets download -d neerugattivikram/ent-surgeon-patient-data-for-medication-analysis \
  -p "$BASE_DIR" --unzip
mv "$BASE_DIR"/ent-surgeon-patient-data-for-medication-analysis/*.csv \
   "$BASE_DIR/ent_patients.csv"
rm -r "$BASE_DIR"/ent-surgeon-patient-data-for-medication-analysis

echo "3️⃣ Downloading disease-prediction symptom data (CSV) from Kaggle..."
python -m kaggle datasets download -d boffinbot/disease-prediction-dataset \
  -p "$BASE_DIR" --unzip
mv "$BASE_DIR"/disease-prediction-dataset/*.csv \
   "$BASE_DIR/disease_prediction.csv"
rm -r "$BASE_DIR"/disease-prediction-dataset

echo "4️⃣ Reminder: Manually download the Diagnostic Errors dataset:"
echo "     → https://data.mendeley.com/datasets/6tgz2db7yn/1"
echo "     and save it as $BASE_DIR/diagnostic_errors.csv"

echo
echo "📂 Final contents of $BASE_DIR:"
ls -1 "$BASE_DIR"
