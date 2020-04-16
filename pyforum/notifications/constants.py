# class Action
class ActionTypes:
    VOTED_UP = "VU"
    VOTED_DOWN = "VD"
    ANSWERED = "A"
    ALSO_ANSWERED = "AC"
    COMMENTED = "C"
    ACCEPTED_ANSWER = "AA"
    SAVED = "S"

    LABELS = {
        VOTED_UP: "đã vote up",
        VOTED_DOWN: "đã vote down",
        ANSWERED: "đã trả lời",
        ALSO_ANSWERED: "cũng đã trả lời",
        COMMENTED: "đã bình luận trả lời",
        ACCEPTED_ANSWER: "đã đánh dấu trả lời",
        SAVED: "đã lưu",
    }

    CHOICES = tuple(LABELS.items())
