#!/bin/bash
python averageanalysis.py &&
python analysis.py &&
python analysiswindows.py &&
python windowanalysis.py &&
python csvanalysis.py &&
python sendemail.py