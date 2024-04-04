from dataclasses import dataclass
from typing import Any, Dict, List, Union

# https://github.com/citation-file-format/citation-file-format/issues/373
DUTCH_NAME_PARTICLES: List[str] = ['den', 'van', 'van den', 'van het',
                                   'op het', "van 't", "op 't", "v/d"]
SPANISH_NAME_PARTICLES: List[str] = ['de', 'de la']

NAME_PARTICLES: List[str] = list(
    set(DUTCH_NAME_PARTICLES + SPANISH_NAME_PARTICLES))

SPLIT_NAME_PARTICLES: List[str] = [p2 for split_particle_list in [
    p1.split(' ') for p1 in NAME_PARTICLES] for p2 in split_particle_list]

NAME_SUFFIXES: List[str] = ['jr.', 'jr', 'sr.', 'sr', 'i',
                            'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']


@dataclass
class Token:
    tag: str
    value: str


def get_tokens(human_name: str) -> List[Token]:
    raw_tokens: List[Token] = [Token(tag="", value=v)
                               for v in human_name.strip().split(sep=' ')]

    tokens: List[Token] = []
    if len(raw_tokens):
        # find suffix
        token = raw_tokens.pop()
        if token.value.casefold() in NAME_SUFFIXES and len(raw_tokens) >= 2:
            token.tag = 'suffix'
            tokens.append(token)
        else:
            raw_tokens.append(token)

        has_last_name: bool = False
        while (True):
            token = raw_tokens.pop()
            if len(raw_tokens) == 0:
                token.tag = 'first_name'
                tokens.append(token)
                break
            elif len(raw_tokens) == 1:
                if has_last_name and token.value.casefold() in NAME_PARTICLES:
                    token.tag = 'particle'
                    tokens.append(token)
                elif has_last_name:
                    token.tag = 'middle_name'
                    tokens.append(token)
                else:
                    token.tag = 'last_name'
                    has_last_name = True
                    tokens.append(token)
            else:
                if has_last_name and token.value.casefold() in NAME_PARTICLES:
                    token.tag = 'particle'
                    tokens.append(token)
                else:
                    # we have at least 2 extra raw tokens

                    # see if the token is the first part of a particle with 2 words
                    # currently this algorithm only handles particles with at most 2 words
                    next_token = raw_tokens.pop()
                    possible_two_word_particle = ' '.join(
                        [next_token.value, token.value]).casefold()
                    if has_last_name and possible_two_word_particle in NAME_PARTICLES:
                        token = Token(
                            tag="particle", value=possible_two_word_particle)
                        tokens.append(token)
                    elif has_last_name is False:
                        raw_tokens.append(next_token)
                        token.tag = 'last_name'
                        has_last_name = True
                        tokens.append(token)
                    else:
                        raw_tokens.append(next_token)

                        # it is either a middle name token or a n-ary last name token
                        # but we will assume it is a middle name token for now
                        token.tag = 'middle_name'

                        # merge middle name with previous token if necessary
                        previous_token = tokens.pop()
                        if previous_token.tag == 'middle_name':
                            token.value = token.value + previous_token.value
                        else:
                            tokens.append(previous_token)

                        # append middle name token
                        tokens.append(token)

        # reverse the tokens so the are in the correct order
        tokens.reverse()
        return tokens
    else:
        return []


def parse_human_name(human_name: str):

    first_name: str = ''
    middle_name: str = ''
    name_particle: str = ''
    last_name: str = ''
    name_suffix: str = ''

    tokens: List[Token] = get_tokens(human_name=human_name)

    for token in tokens:
        if token.tag == 'first_name':
            first_name += ' ' + token.value
        elif token.tag == 'middle_name':
            middle_name += ' ' + token.value
        elif token.tag == 'particle':
            name_particle += ' ' + token.value
        elif token.tag == 'last_name':
            last_name += ' ' + token.value
        elif token.tag == 'suffix':
            name_suffix += ' ' + token.value

    return first_name.strip(), middle_name.strip(), name_particle.strip(), last_name.strip(), name_suffix.strip()


def is_human_name(name: str) -> bool:
    return len(name) > 1
