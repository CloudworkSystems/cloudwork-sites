# Clips for the story site

A one-off helper that makes a few wordless atmosphere clips (dawn, noon, dusk,
night) through fal.ai for the True Convo story site.

This is website work only. It is not how True Convo will make media. In the
product, paid generation is always optional: the person can use their own key,
a free local model, or upload their own clip, and the capability lives in the
portable capability layer so any model can use it.

- `shots.json`: the shot list, the model, the price per clip and the spending cap.
- `make_clips.py`: dry run by default. It refuses to spend while the price is
  missing, when a run would pass the cap, or when `FAL_KEY` is not set.
- `log.jsonl`: every prompt, estimate and result, written as it happens.

Raw clips land in `trueconvo-day/media/raw/`. They are compressed and checked
at phone and desktop width before any page uses them.
