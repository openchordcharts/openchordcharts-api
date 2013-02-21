# -*- coding: utf-8 -*-


"""Chord rendering functions."""


import itertools

from markupsafe import Markup

from . import music_theory


def render_parts(chart, chords_per_row, from_key=None, to_key=None):
    parts = []
    for part_name, part_occurence in iter_parts_with_occurences(chart):
        part_rows = []
        part_chords = chart.parts[part_name]
        part_idx = 0
        while part_idx < len(chart.parts[part_name]):
            row_chords = part_chords[part_idx:part_idx + chords_per_row]
            rendered_row_chords = iter_rendered_chords(row_chords, from_key, to_key) \
                if part_occurence == 0 \
                else list(itertools.repeat(u'—', chords_per_row))
            part_rows.append(rendered_row_chords)
            part_idx += chords_per_row
        parts.append({
            'name': part_name,
            'occurence': part_occurence,
            'rows': part_rows,
            })
    return parts


def iter_parts_with_occurences(chart):
    nb_occurences_per_part_name = {}
    for part_name in chart.structure:
        if part_name in nb_occurences_per_part_name:
            nb_occurences_per_part_name[part_name] += 1
        else:
            nb_occurences_per_part_name[part_name] = 0
        yield part_name, nb_occurences_per_part_name[part_name]


def iter_rendered_chords(chords, from_key=None, to_key=None):
    previous_chord = chords[0]
    yield render_chord(
        music_theory.compute_transposed_chord(previous_chord, from_key, to_key)
        if from_key is not None and to_key is not None and from_key != to_key
        else previous_chord
        )
    for chord in chords[1:]:
        if chord == previous_chord:
            yield u'—'
        else:
            yield render_chord(
                music_theory.compute_transposed_chord(chord, from_key, to_key)
                if from_key is not None and to_key is not None and from_key != to_key
                else chord
                )
        previous_chord = chord


def render_chord(chord):
    rendered_chord = chord
    if rendered_chord.endswith('b5'):
        rendered_chord = rendered_chord[:-2] + Markup(u'<sup>{0}</sup>'.format(rendered_chord[-2:]))
    # FIXME This is not semantic, I have to rewrite the font!
    rendered_chord = rendered_chord.replace('#', '<')
    rendered_chord = rendered_chord.replace('b', '>')
    return rendered_chord