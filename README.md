Board Game Reinforcement Learning ที่อ้างอิงจาก [AlphaZero](https://arxiv.org/pdf/1712.01815.pdf) ของ [Deepmind](https://deepmind.com/blog/alphago-zero-learning-scratch/)

# เกม
* หมากฮอส (Makhos / Thai Checkers)
* โอเทลโล่ (Othello / Reversi)
* Connect Four
* โอ-เอ็กซ์ (Tic-tac-toe)

# วิธีใช้งาน

## ความต้องการ

* Python 2.7+ หรือ Python 3.6+
* Keras 2.1+
* Tensorflow

## Setup

```
pip install -r requirements.txt
```

## ลองเล่นกับ pretrained model

```
python run.py arena makhos human mcts,data/makhos/model-45k.h5,1000
```

## สร้าง Model
```
python run.py newmodel <game> model.h5
```

## Self-play
เล่นกับตัวเอง 5,000 เกม โดยแต่ละตาที่เดินมีการซิมมูเลชั่น 100 ครั้ง และเซฟข้อมูลเกมลงไฟล์ selfplay.txt
```
python run.py generate <game> --model model.h5 --simulation 100 -n 5000 --file selfplay.txt --progress
```

## Training
ทำการเทรนโมเดล model.h5 ด้วยไฟล์ข้อมูล selfplay.txt จำนวน 3 epochs และเซฟใส่ newmodel.h5
```
python run.py train <game> selfplay.txt model.h5 newmodel.h5 --epoch 3 --progress
```

## ทดสอบ

```
python run.py arena <game> <player1> <player2>
```
โดยที่
* game มีค่าเป็น `makhos`, `othello`, `c4`, `ox`
* player1 และ player2 มีค่าเป็น
  * `human` เลือกตาเดินจากคีย์บอร์ด
  * `mcts,model.h5,1000` เลือกตาเดนถัดไปโดยใช้ policy network + value network จาก model.h5 และใช้ MCTS ที่มีจำนวนซิมมูเลชั่น 1,000 ครั้ง
  * `policy,model.h5` เลือกตาเดินโดยใช้แต่ policy network ของ model.h5
