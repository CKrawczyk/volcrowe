from collections import Counter
from stats.models import *
import json
import stats
static_path = stats.__path__[0]+'/static/'
with open(static_path+'city_location.json', 'r') as f:
    map_locations = json.load(f)

answer_lookup = {
    'GN': {
        'location': 'answerGender__answer',
        'answers': {
            'M': 'Male',
            'F': 'Female'
        },
        'reverse': {
            'Male': 'M',
            'Female': 'F',
        }
    },
    'YN': {
        'location': 'answerBool__answer',
        'answers': {
            0: False,
            1: True,
        },
        'reverse': {
            'false': 0,
            'true': 1,
        },
    },
    'AD': {
        'location': 'answerAD__answer',
        'answers': {
            0: 'Perfer not to answer',
            1: 'Strongly disagree',
            2: 'Dissagree',
            3: 'Somewhat disagree',
            4: 'Neither agree or disagree',
            5: 'Somewhat agree',
            6: 'Agree',
            7: 'Strongly agree',
        },
        'reverse': {
            'Perfer not to answer': 0,
            'Strongly disagree': 1,
            'Dissagree': 2,
            'Somewhat disagree': 3,
            'Neither agree or disagree': 4,
            'Somewhat agree': 5,
            'Agree': 6,
            'Strongly agree': 7,
        }
    },
    'ED': {
        'location': 'answerEdu__answer',
        'answers': {
            0: 'Blank',
            1: 'No education',
            2: 'Primary education',
            3: 'Lower secondary education',
            4: 'Upper secondary education',
            5: 'Post secondary non-tertiary education',
            6: 'Short cycle tertiary education',
            7: 'Bachelors Degree or equivalent',
            8: 'Masters Degree or equivalent',
            9: 'Doctoral Degree or  equivalent',
        },
        'reverse': {
            'Blank': 0,
            'No education': 1,
            'Primary education': 2,
            'Lower secondary education': 3,
            'Upper secondary education': 4,
            'Post secondary non-tertiary education': 5,
            'Short cycle tertiary education': 6,
            'Bachelors Degree or equivalent': 7,
            'Masters Degree or equivalent': 8,
            'Doctoral Degree or  equivalent': 9,
        }
    },
    'ET': {
        'location': 'answerEthnicity__answer',
        'answers': {
            'W': 'White/Caucasian',
            'O': 'Other',
            'SA': 'South Asian',
            'EA': 'East Asian',
            'M': 'Mixed',
            'HL': 'Hispanice/Latino',
            'C': 'Caribbean',
            'ME': 'Middle Eastern',
            'BA': 'Black African',
            'A': 'Amerindian',
        },
        'reverse': {
            'White/Caucasian': 'W',
            'Other': 'O',
            'South Asian': 'SA',
            'East Asian': 'EA',
            'Mixed': 'M',
            'Hispanice/Latino': 'HL',
            'Caribbean': 'C',
            'Middle Eastern': 'ME',
            'Black African': 'BA',
            'Amerindian': 'A',
        }
    },
    'QU': {
        'location_confidence': 'answerQuiz__confidence',
        'location_score': 'answerQuiz__score',
        'answers': {
            1: 'Very unconfident',
            2: 'Unconfident',
            3: 'Somewhat unconfident',
            4: 'Neither confident or unconfident',
            5: 'Somewhat confident',
            6: 'Confident',
            7: 'Very confident',
        },
        'reverse': {
            'Very unconfident': 1,
            'Unconfident': 2,
            'Somewhat unconfident': 3,
            'Neither confident or unconfident': 4,
            'Somewhat confident': 5,
            'Confident': 6,
            'Very confident': 7,
        }
    },
    'OP': {
        'location': 'answerOpen__answer',
    }
}


def cast_value(s):
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return s


def get_aggregation(ret, fields, context, instance):
    request_params = context['request'].query_params.dict()
    filter_set = {
        'question__number': instance.number
    }
    for key, value in request_params.iteritems():
        if (key not in fields.keys()) and (key not in ['format', 'ordering']):
            if ('__in' in key):
                filter_set[key] = value.split(',')
            else:
                filter_set[key] = value
    kind = instance.kind.kind
    plot_type = instance.plot_type
    lookup = answer_lookup[kind]
    ans = Answer.objects.filter(**filter_set)
    ret['count'] = ans.count()
    if plot_type == 'P':
        val = ans.values(lookup['location'])
        ret['results'] = Counter([lookup['answers'][a[lookup['location']]] for a in val])
    elif plot_type == 'H':
        val = ans.values(lookup['location'])
        ret['results'] = [cast_value(a[lookup['location']]) for a in val]
    elif plot_type == 'M':
        val = ans.values(lookup['location'])
        lat_all = []
        lon_all = []
        city_all = []
        for a in val:
            city = a[lookup['location']].lower()
            if city in map_locations:
                geo = map_locations[city]
                lat_all.append(geo['lat'])
                lon_all.append(geo['lng'])
                city_all.append(city)
        c = Counter(zip(lat_all, lon_all, city_all))
        lat = []
        lon = []
        city = []
        count = []
        for key, value in c.iteritems():
            lat.append(key[0])
            lon.append(key[1])
            city.append(key[2])
            count.append(value)
        ret['results'] = {
            'lat': lat,
            'lon': lon,
            'city': city,
            'count': count,
        }
    else:
        val = ans.values(lookup['location_score'], lookup['location_confidence'])
        count = Counter(['{0}, {1}'.format(a[lookup['location_score']], a[lookup['location_confidence']]) for a in val])
        ret['results'] = {
            'confidence': [a[lookup['location_confidence']] for a in val],
            'scores': [a[lookup['location_score']] for a in val],
            'confidence_map': lookup['answers'],
            'count': count,
        }
    return ret
