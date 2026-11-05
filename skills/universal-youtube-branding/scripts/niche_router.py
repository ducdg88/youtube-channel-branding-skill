#!/usr/bin/env python3
"""Suggest a seed style from niche words, without claiming a trained classifier.
Usage: python niche_router.py --niche "Luxury Woodworking" --output brand_suggestion.json
For unknown niches, return neutral baseline and request semantic creative-director review.
"""
import argparse,json,re,pathlib
P=pathlib.Path(__file__).resolve().parents[1]
def main():
 a=argparse.ArgumentParser();a.add_argument('--niche',required=True);a.add_argument('--output');ns=a.parse_args()
 library=json.loads((P/'templates/niche_style_library.json').read_text(encoding='utf-8'))
 txt=ns.niche.lower();scores={}
 for k,v in library.items():
  scores[k]=sum(2 if kw in txt else 0 for kw in v['keywords'])
  if v['name'].lower() in txt:scores[k]+=4
 best=max(scores,key=scores.get)
 if scores[best]==0:
  result={'input_niche':ns.niche,'style_source':'fallback_neutral','manual_creative_review_required':True,'palette':{'background':'#13191E','surface':'#253139','accent':'#C49A58','highlight':'#F5D8AB','text':'#FFFFFF'},'motif':'choose metaphor based on actual niche','scene':'requires niche-specific direction'}
 else:
  d=library[best]
  result={'input_niche':ns.niche,'style_source':'keyword_heuristic','matched_preset':best,'confidence_note':'heuristic selection, not an AI classification guarantee','manual_creative_review_required':False,'palette':d['palette'],'motif':d['motif'],'emotional_tone':d['emotional_tone'],'scene':d['scene']}
 out=json.dumps(result,ensure_ascii=False,indent=2)
 if ns.output:pathlib.Path(ns.output).write_text(out,encoding='utf-8')
 print(out)
if __name__=='__main__':main()
