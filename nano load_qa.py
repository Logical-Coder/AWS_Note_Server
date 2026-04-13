import os
import django

# ?? SET YOUR DJANGO SETTINGS PATH
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from notes.models import QANote, Answer


def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('---')

    for block in blocks:
        lines = block.strip().split('\n')

        data = {
            "type": "other",
            "subtopic": "",
            "format": "description",
            "question": "",
            "answers": []
        }

        current_answer = ""

        for line in lines:
            line = line.strip()

            if line.startswith("TYPE:"):
                data["type"] = line.replace("TYPE:", "").strip()

            elif line.startswith("SUBTOPIC:"):
                data["subtopic"] = line.replace("SUBTOPIC:", "").strip()

            elif line.startswith("FORMAT:"):
                data["format"] = line.replace("FORMAT:", "").strip()

            elif line.startswith("QUESTION:"):
                data["question"] = line.replace("QUESTION:", "").strip()

            elif line.startswith("ANSWER:"):
                if current_answer:
                    data["answers"].append(current_answer.strip())
                current_answer = line.replace("ANSWER:", "").strip()

            else:
                current_answer += " " + line

        if current_answer:
            data["answers"].append(current_answer.strip())

        # ?? SAVE TO DATABASE
        if data["question"]:
            note = QANote.objects.create(
                question=data["question"],
                question_type=data["type"],
                question_subtopic=data["subtopic"],
                question_format=data["format"]
            )

            for ans in data["answers"]:
                Answer.objects.create(
                    question=note,
                    answer_text=ans
                )

            print(f"? Saved: {data['question'][:50]}")

    print("\n?? DONE IMPORTING DATA")


if __name__ == "__main__":
    file_path = "data.txt"  # your input file
    parse_file(file_path)