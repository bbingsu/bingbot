import os
isChatterAvailable = True
try:
  import tensorflow as tf
  from transformers import TFGPT2LMHeadModel, AutoTokenizer


  THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
  MODEL_PATH = os.path.join(THIS_FOLDER, 'gpt2_model_chatbot')
  model = TFGPT2LMHeadModel.from_pretrained(MODEL_PATH)
  tokenizer = AutoTokenizer.from_pretrained('skt/kogpt2-base-v2', bos_token='</s>', eos_token='</s>', pad_token='<pad>')

  def answer_by_chatbot(user_text) -> str:
    sent = '<usr>' + user_text + '<sys>'
    input_ids = [tokenizer.bos_token_id] + tokenizer.encode(sent)
    input_ids = tf.convert_to_tensor([input_ids])
    output = model.generate(input_ids, max_length=50, do_sample=True, top_k=20)
    sentence = tokenizer.decode(output[0].numpy().tolist())
    chatbot_response = sentence.split('<sys> ')[1].replace('</s>', '')
    return chatbot_response
except:
  isChatterAvailable = False

  def answer_by_chatbot(user_text) -> str:
    return '아직 설치되지 않았어요. 잠시 후 다시 시도해주세요.'