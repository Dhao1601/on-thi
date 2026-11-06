"""Gộp các file JSON câu hỏi (mỗi đề một file) thành data.js cho trang ôn thi.

Chạy: python3 build_data.py <thư-mục-chứa-json> [overrides.json]
(overrides: đáp án đã kiểm tra lại, theo id câu hỏi)
"""
import json, os, re, sys, glob

SRC = sys.argv[1]
OVER = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else {}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.js')

SUBJECTS = [
    ('AET', 'AET102', 'Art Appreciation (đề tiếng Anh)', 'AET-de*.json'),
    ('HOD', 'HOD102', 'History of Design (đề tiếng Anh)', 'HOD-de*.json'),
    ('IPR', 'IPR', 'Intellectual Property Rights (đề tiếng Anh)', 'IPR-de*.json'),
    ('MLN131', 'MLN131', 'Chủ nghĩa xã hội khoa học', 'MLN131.json'),
]
AI_NOTE = ('Đề gốc không kèm đáp án. Mỗi câu được giải độc lập 2 lần; câu nào lệch nhau hoặc lệch '
           'đáp án bình luận FUOverflow thì được phân xử lại (có xem ảnh gốc, tra cứu). '
           'Câu đánh dấu ⚠️ là câu vẫn còn chưa chắc chắn.')


def clean_answer(a):
    if isinstance(a, str):
        a = re.split(r'[,\s;/]+', a)
    return sorted({x.strip().upper() for x in a if x and x.strip()})


subjects = []
for sid, code, name, pattern in SUBJECTS:
    files = sorted(glob.glob(os.path.join(SRC, pattern)), key=lambda p: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p)])
    sets = []
    for f in files:
        raw = json.load(open(f, encoding='utf-8'))
        m = re.search(r'de(\d+)', os.path.basename(f))
        set_id = f'de{m.group(1)}' if m else 'bo'
        set_name = f'Đề {m.group(1)}' if m else 'Bộ câu hỏi'
        qs = []
        for n, q in enumerate(raw, 1):
            if not q.get('question') or not q.get('options'):
                continue
            opts = [{'key': o['key'].strip().upper(), 'text': o['text'].strip()} for o in q['options'] if o.get('text')]
            ans = [a for a in clean_answer(q.get('answer', [])) if a in {o['key'] for o in opts}]
            if not ans:
                continue
            qid = f'{sid}-{set_id}-{q.get("id", n)}'
            ov = OVER.get(qid, {})
            if ov.get('answer'):
                ans = [a for a in clean_answer(ov['answer']) if a in {o['key'] for o in opts}] or ans
            qs.append({
                'id': qid,
                'question': q['question'].strip(),
                'options': opts,
                'answer': ans,
                'multi': bool(q.get('multi')) or len(ans) > 1,
                'confidence': ov.get('confidence') or q.get('confidence', 'medium'),
                'source': q.get('source', 'ai'),
                'explanation': ov.get('explanation') or q.get('explanation') or '',
                'key_fact': ov.get('key_fact') or '',
                'topic': ov.get('topic') or '',
                'note': ov.get('note') or '',
                'comment_answer': q.get('comment_answer') or None,
            })
        if qs:
            sets.append({'id': set_id, 'name': set_name, 'questions': qs})
    if sets:
        note = None if sid == 'MLN131' else AI_NOTE
        subjects.append({'id': sid, 'code': code, 'name': name, 'note': note, 'sets': sets})

data = {
    'subjects': subjects,
    'note': 'Nguồn câu hỏi: thư mục "file đề đáp án các môn" trên Google Drive. '
            'MLN131 dùng đáp án gốc (đã soát lại); AET, HOD, IPR có đáp án do AI giải và kiểm tra chéo.',
}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('window.QUIZ_DATA = ')
    json.dump(data, fh, ensure_ascii=False)
    fh.write(';\n')

for s in subjects:
    print(s['code'], [(st['id'], len(st['questions'])) for st in s['sets']])
print('->', OUT)
