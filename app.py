import os
import re

import tensorflow as tf
from flask import Flask, request, jsonify

from settings import PROJECT_ROOT
from chatbot.botpredictor import BotPredictor

app = Flask(__name__)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')

NOT_UNDERSTOOD = 'pardon?'

with tf.Session() as sess:
    predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir,
                            result_dir=res_dir, result_file='basic')

    @app.route('/chatbot', methods=['GET', 'POST'])
    def Question():
        try:
            session_id = int(request.args.get('previous_session_id', 1))
            predictor.session_data.get_session(session_id)
        except Exception as e:
            print(e)
            session_id = predictor.session_data.add_session()
        
        question_sentence = request.args.get('sentence', '')
        answer = NOT_UNDERSTOOD
        if question_sentence:
            answer = re.sub(r'_nl_|_np_', ' ', predictor.predict(session_id, question_sentence)).strip()
        return jsonify({
            'question': question_sentence,
            'answer': answer,
            'current_session_id': session_id,
            'okay': answer != NOT_UNDERSTOOD,
        })

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80, debug=True)
