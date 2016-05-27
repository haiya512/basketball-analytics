import os
import sys
sys.path.append(os.path.abspath('.'))

import datetime
from collections import defaultdict
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Date, Time, \
                       UniqueConstraint, create_engine, tuple_, or_, and_, func
from sqlalchemy.types import Boolean, Array
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import numpy as np 

from model import Session, Base, enums
from model.stats import TeamMatchStats, TeamSeasonStats, TeamSeasonHomeStats, TeamSeasonAwayStats


class GoalAttempt(Base):
    __tablename__ = 'goal_attempts'

	id = Column(Integer, primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	start = Column(Geometry('POINT'))
	end = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	assisted_by = Column(ForeignKey('players.id'), index=True)
	pass_graph = Column(Array(Integer))
	is_own = Column(Boolean)
	shot = Column(Boolean)
	headed = Column(Boolean)
	#action_type: type of pass. enum
	#coordinates: ??
	#middle: ??
	#swere: ??


class Pass(Base):
	__tablename__ = 'passes'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	start = Column(Geometry('POINT'))
	end = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	assist = Column(Boolean)
	headed = Column(Boolean)
	key_pass = Column(Boolean)
	long_ball = Column(Boolean)
	through_ball = Column(Boolean)
	throw_ins = Column(Boolean)
	# action_type: type of pass. [Possession]
	# type = outcome enum


class Cross(Base):
	__tablename__ = 'passes'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	start = Column(Geometry('POINT'))
	end = Column(Geometry('POINT'))
	key_pass = Column(Boolean)
	# type: outcome of the cross enum


class Dribble(Base):
	__tablename__ = 'dribbles'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players.id'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	other_player_id = Column(ForeignKey('players.id'), index=True)
	other_team_id = Column(ForeignKey('teams.id'), index=True)
	
	# type: outcome of dribble enum
	# action_type: type of action [Attack, Defense]


class Tackle(Base):
	__tablename__ = 'tackles'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injurytime_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	# player_id = 
	# team_id = Column(ForeignKey('teams.id'), index=True)
	# tackler_id = 
	# tackler_team_id = Column(ForeignKey('teams.id'), index=True)
	# action_type
	# type: outcome of tackle enum


class HeadedDual(Base):
	__tablename__ = 'headed_duals'

	id = Column(primary_key=True)
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injury_time_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	other_player_id = Column(ForeignKey('players'), index=True)
	# action_type
	# type: outcome of tackle enum


class Interception(Base):
	__tablename__ = 'interceptions'
	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injury_time_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	headed = Column(Boolean)
	# action_type


class Clearance(Base):
	__tablename__ = 'clearances'

	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injury_time_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	headed = Column(Boolean)
	# action_type


class Foul(Base):
	__tablename__ = 'fouls'

	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injury_time_play = Column(Boolean)
	loc = Column(Geometry('POINT'))
	player_id = Column(ForeignKey('players'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)
	other_player_id = Column(ForeignKey('players.id'), index=True)


class Card(Base):
	__tablename__ = 'cards'

	mins = Column(Integer)
	secs = Column(Integer)
	minsecs = Column(Integer)
	injury_time_play = Column(Boolean)
	# type = cards enum
	player_id = Column(ForeignKey('players'), index=True)
	team_id = Column(ForeignKey('teams.id'), index=True)


class BlockedPass(Base):
	__tablename__ = 'blocks_passes'

	action_type
	coordinates
	end
	headed
	injurytime_play
	loc
	middle
	player_id
	mins
	minsec
	secs
	shot
	shot_player
	shot_team
	start
	team_id
	type


class BlockedCross(Base):
	__tablename__ = 'blocked_crosses'

	action_type
	coordinates
	end
	headed
	injurytime_play
	loc
	middle
	player_id
	mins
	minsec
	secs
	shot
	shot_player
	shot_team
	start
	team_id
	type


class BlockedShot(Base):
	__tablename__ = 'blocked_crosses'

	action_type
	coordinates
	end
	headed
	injurytime_play
	loc
	middle
	player_id
	mins
	minsec
	secs
	shot
	shot_player
	shot_team
	start
	team_id
	type


class GoalKeep(Base):
	__tablename__ = 'goalkeeping'

	action_type
	headed
	injurytime_play
	player_id
	team_id


class Offside(Base):
	__tablename__ = 'offsides'

	mins
	minsec
	player_id
	secs
	team
