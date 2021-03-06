CUDA_VISIBLE_DEVICES=0 python main.py \
  --data_dir ../../../data/QDGAT \
  --save_dir "output" \
  --batch_size 16 \
  --eval_batch_size 5 \
  --max_epoch 5 \
  --do_eval \
  --warmup 0.06 \
  --optimizer adam \
  --learning_rate 1e-4 \
  --weight_decay 5e-5 \
  --seed 1117 \
  --gradient_accumulation_steps 8 \
  --bert_learning_rate 1.5e-5 \
  --bert_weight_decay 0.01 \
  --log_per_updates 100 \
  --eps 1e-6 \
  --roberta_model roberta-base \
  --pre_path "output"