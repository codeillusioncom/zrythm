/*
 * Copyright (C) 2018-2019 Alexandros Theodotou
 *
 * This file is part of Zrythm
 *
 * Zrythm is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Zrythm is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Zrythm.  If not, see <https://www.gnu.org/licenses/>.
 */

#include "audio/channel.h"
#include "audio/chord_track.h"
#include "audio/mixer.h"
#include "audio/tracklist.h"
#include "audio/track.h"
#include "gui/widgets/arranger.h"
#include "gui/widgets/bot_dock_edge.h"
#include "gui/widgets/center_dock.h"
#include "gui/widgets/main_window.h"
#include "gui/widgets/mixer.h"
#include "gui/widgets/timeline_arranger.h"
#include "gui/widgets/tracklist.h"
#include "project.h"
#include "utils/arrays.h"

/**
 * Initializes the tracklist.
 *
 * Note: mixer and master channel/track, chord track and
 * each channel must be initialized at this point.
 */
void
tracklist_init (Tracklist * self,
                int loading)
{
  g_warn_if_fail (MIXER);
  g_warn_if_fail (MIXER->master);
  g_warn_if_fail (MIXER->master->track);

  if (loading)
    {
      for (int i = 0; i < self->num_tracks; i++)
        self->tracks[i] =
          project_get_track (
            self->track_ids[i]);

      return;
    }

  /* add master track */
  tracklist_append_track ((Track *) MIXER->master->track);

  /* add chord track */
  g_warn_if_fail (P_CHORD_TRACK);
  tracklist_append_track (P_CHORD_TRACK);

  /* add each channel */
  for (int i = 0; i < MIXER->num_channels; i++)
    {
      Channel * channel = MIXER->channels[i];
      g_warn_if_fail (channel);
      g_warn_if_fail (channel->track);
      tracklist_append_track (channel->track);
    }
}

/**
 * Finds visible tracks and puts them in given array.
 */
void
tracklist_get_visible_tracks (Track **    visible_tracks,
                              int *       num_visible)
{
  *num_visible = 0;
  for (int i = 0; i < TRACKLIST->num_tracks; i++)
    {
      Track * track = TRACKLIST->tracks[i];
      if (track->visible)
        {
          visible_tracks[*num_visible++] = track;
        }
    }
}

int
tracklist_contains_master_track ()
{
  for (int i = 0; TRACKLIST->num_tracks; i++)
    {
      Track * track = TRACKLIST->tracks[i];
      if (track->type == TRACK_TYPE_MASTER)
        return 1;
    }
  return 0;
}

int
tracklist_contains_chord_track ()
{
  for (int i = 0; TRACKLIST->num_tracks; i++)
    {
      Track * track = TRACKLIST->tracks[i];
      if (track->type == TRACK_TYPE_CHORD)
        return 1;
    }
  return 0;
}

Track *
get_track_by_name (
  Tracklist * self,
  const char * name)
{
  Track * track;
  for (int i = 0; i < self->num_tracks; i++)
    {
      track = self->tracks[i];
      if (g_strcmp0 (track->name, name) == 0)
        return track;
    }
  return NULL;

}

void
set_track_name (Tracklist * self, Track * track)
{
  int count = 1;
  char * new_label = g_strdup (track->name);
  while (get_track_by_name (self, new_label))
    {
      g_free (new_label);
      new_label =
        g_strdup_printf ("%s %d",
                         track->name,
                         count++);
    }
  track->name = new_label;
}

/**
 * Adds given track to given spot in tracklist.
 */
void
tracklist_add_track (Track *     track,
                     int         pos)
{
  g_warn_if_fail (track->id > -1);

  set_track_name (TRACKLIST, track);

  array_insert (TRACKLIST->tracks,
                TRACKLIST->num_tracks,
                pos,
                track);
  int size = TRACKLIST->num_tracks - 1;
  array_insert (TRACKLIST->track_ids,
                size,
                pos,
                track->id);

  EVENTS_PUSH (ET_TRACK_ADDED, track);
}

ChordTrack *
tracklist_get_chord_track ()
{
  Track * track;
  for (int i = 0; i < TRACKLIST->num_tracks; i++)
    {
      track = TRACKLIST->tracks[i];
      if (track->type == TRACK_TYPE_CHORD)
        {
          return (ChordTrack *) track;
        }
    }
  g_warn_if_reached ();
  return NULL;
}

void
tracklist_append_track (Track *     track)
{
  set_track_name (TRACKLIST, track);

  TRACKLIST->track_ids[TRACKLIST->num_tracks] =
    track->id;
  array_append (TRACKLIST->tracks,
                TRACKLIST->num_tracks,
                track);

  g_message ("track id %d", track->id);
  g_warn_if_fail (track->id > -1);
}

int
tracklist_get_track_pos (Track *     track)
{
  return array_index_of ((void **) TRACKLIST->tracks,
                         TRACKLIST->num_tracks,
                         (void *) track);
}

int
tracklist_get_last_visible_pos ()
{
  for (int i = TRACKLIST->num_tracks - 1; i >= 0; i--)
    {
      if (TRACKLIST->tracks[i]->visible)
        {
          return i;
        }
    }
  g_warn_if_reached ();
  return -1;
}

Track*
tracklist_get_last_visible_track ()
{
  for (int i = TRACKLIST->num_tracks - 1; i >= 0; i--)
    {
      if (TRACKLIST->tracks[i]->visible)
        {
          return TRACKLIST->tracks[i];
        }
    }
  g_warn_if_reached ();
  return NULL;
}

Track *
tracklist_get_first_visible_track ()
{
  for (int i = 0; i < TRACKLIST->num_tracks; i++)
    {
      if (TRACKLIST->tracks[i]->visible)
        {
          return TRACKLIST->tracks[i];
        }
    }
  g_warn_if_reached ();
  return NULL;
}

Track *
tracklist_get_prev_visible_track (Track * track)
{
  for (int i = tracklist_get_track_pos (track);
       i >= 0; i--)
    {
      if (TRACKLIST->tracks[i]->visible)
        {
          return TRACKLIST->tracks[i];
        }
    }
  g_warn_if_reached ();
  return NULL;
}

Track *
tracklist_get_next_visible_track (Track * track)
{
  for (int i = tracklist_get_track_pos (track);
       i < TRACKLIST->num_tracks; i++)
    {
      if (TRACKLIST->tracks[i]->visible)
        {
          return TRACKLIST->tracks[i];
        }
    }
  g_warn_if_reached ();
  return NULL;
}

void
tracklist_remove_track (Track *     track)
{
  /* stop engine and give it some time to stop
   * running */
  int prev = g_atomic_int_get (&AUDIO_ENGINE->run);
  g_atomic_int_set (&AUDIO_ENGINE->run, 0);
  if (prev)
    g_usleep (1000);

  mixer_remove_channel (track->channel);
  array_delete (TRACKLIST->tracks,
                TRACKLIST->num_tracks,
                track);
  int size = TRACKLIST->num_tracks + 1;
  array_delete (TRACKLIST->track_ids,
                size,
                track->id);
  tracklist_selections_remove_track (
    TRACKLIST_SELECTIONS, track);
  project_remove_track (track);
  track_free (track);

  EVENTS_PUSH (ET_TRACK_REMOVED,
               NULL);

  mixer_recalculate_graph (MIXER, 1);

  g_atomic_int_set (&AUDIO_ENGINE->run, prev);
}
