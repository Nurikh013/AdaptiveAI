def analyze_quiz(results):
  stats={}
  for topic, is_correct in results:
    if topic not in stats:
      stats[topic]={'total':0, 'correct':0}
    stats[topic]['total']+=1
    if is_correct:
      stats[topic]['correct']+=1
  percetages={
    topic:round((data['correct']/data['total'])*100,1)
    for topic, data in stats.items()}
  return percetages

  
def find_weakest_topic(percentages):
    if not percentages:
        return None

    return min(percentages, key=percentages.get)

def generate_recommendations(percentages):
    recommendations = {}

    for topic, score in percentages.items():
        if score < 50.0:
            recommendations[topic] = "Needs urgent practice"
        elif score < 80.0:
            recommendations[topic] = "Needs improvement"
        else:
            recommendations[topic] = "Good progress"

    return recommendations
def student_report(results):
  scores=analyze_quiz(results)
  weakest=find_weakest_topic(scores)
  recommendations=generate_recommendations(scores)
  report={
    "scores": scores,
    "recommendations": recommendations,
    "weakest_topic": weakest }
  return report
  

  
  
quiz_results = [
      ("recursion", False),
      ("recursion", True),
      ("recursion", False),
      ("lists", True),
      ("lists", True),
      ("functions", True),
      ("functions", False),
      ("functions", True)
  ]
  
print(student_report(quiz_results))
