from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 2
    ENDOWMENT = cu(20)
    MULTIPLIER_A = 0.3
    MULTIPLIER_B = 0.6

    TYPE_A = 'Type_A'
    TYPE_B = 'Type_B'

    ID1_ROLE = 'Type_A'
    ID2_ROLE = 'Type_B'
    ID3_ROLE = 'Type_B'
    ID4_ROLE = 'Type_A'

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    total_contribution = models.CurrencyField()
    final_payoff_round = models.IntegerField()

class Player(BasePlayer):

    def chat_nickname(self):
        return 'P{}({})'.format(self.id_in_group,self.role)
  
    def chats(self):
        if self.role == C.TYPE_A:
            channel_ST = '{}-{}'.format(self.group.id,'A' )
            return channel_ST
        else:
            channel_ST = '{}-{}'.format(self.group.id,'B' )
            return channel_ST

    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT
    )
    # 定义c初次向其他人分配的点数
    PointsGived1 = models.CurrencyField(initial=0)
    PointsGived2 = models.CurrencyField(initial=0)
    PointsGived3 = models.CurrencyField(initial=0)
    PointsGived4 = models.CurrencyField(initial=0)

    # 定义第二次向其他人追加的点数
    PointsAdded1 = models.CurrencyField(initial=0)
    PointsAdded2 = models.CurrencyField(initial=0)
    PointsAdded3 = models.CurrencyField(initial=0)
    PointsAdded4 = models.CurrencyField(initial=0)
    SubmittedOnce = models.BooleanField(initial=False)

    # 定义从其他人获得的点数
    PointsReceived1 = models.CurrencyField(initial=0)
    PointsReceived2 = models.CurrencyField(initial=0)
    PointsReceived3 = models.CurrencyField(initial=0)
    PointsReceived4 = models.CurrencyField(initial=0)
    TotalReceived = models.CurrencyField(initial=0)

def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    for p in players:
        if p.role == 'Type A':
            p.payoff = C.ENDOWMENT - p.contribution + group.total_contribution * C.MULTIPLIER_A
        else:
            p.payoff = C.ENDOWMENT - p.contribution + group.total_contribution * C.MULTIPLIER_B

def calculate_allocation1(group: Group):
    players = group.get_players()
    for p in players:
        my_id = p.id_in_group
        p.PointsReceived1 = getattr(group.get_player_by_id(1),f'PointsGived{my_id}')
        p.PointsReceived2 = getattr(group.get_player_by_id(2),f'PointsGived{my_id}')
        p.PointsReceived3 = getattr(group.get_player_by_id(3),f'PointsGived{my_id}')
        p.PointsReceived4 = getattr(group.get_player_by_id(4),f'PointsGived{my_id}')
        p.TotalReceived = p.PointsReceived1 + p.PointsReceived2 + p.PointsReceived3 + p.PointsReceived4
# PAGES      
class Chat(Page):
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2
 
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

class ContributionWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class ContributionFeedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        
        return {
            'money_kept': C.ENDOWMENT-player.contribution,
            'individual_share': player.payoff+player.contribution-C.ENDOWMENT
        }

class AllocationStage1(Page):
    form_model = 'player'
    form_fields = ['PointsGived1','PointsGived2','PointsGived3','PointsGived4']
    @staticmethod
    def error_message(player, values):
        group = player.group
        if values['PointsGived1'] > group.get_player_by_id(1).payoff:
            return "The points you assign to player1 cannot exceed its earnings from the contribution stage."
        elif values['PointsGived2'] > group.get_player_by_id(2).payoff:
            return "The points you assign to player2 cannot exceed its earnings from the contribution stage."
        elif values['PointsGived3'] > group.get_player_by_id(3).payoff:
            return "The points you assign to player3 cannot exceed its earnings from the contribution stage."
        elif values['PointsGived4'] > group.get_player_by_id(4).payoff:
            return "The points you assign to player4 cannot exceed its earnings from the contribution stage."
        else:
            pass
    
class AllocationStage1WaitPage(WaitPage):
     after_all_players_arrive = 'calculate_allocation1'

class AllocationStage2(Page):
    timeout_seconds = 180
    form_model = 'player'
    form_fields = ['PointsAdded1','PointsAdded2','PointsAdded3','PointsAdded4']
    @staticmethod
    def live_method(player, data):

        group = player.group
        player.PointsAdded1 = data['PointsAdded1']
        player.PointsAdded2 = data['PointsAdded2']
        player.PointsAdded3 = data['PointsAdded3']
        player.PointsAdded4 = data['PointsAdded4']
        
        player.PointsGived1 = player.PointsGived1 + player.PointsAdded1
        player.PointsGived2 = player.PointsGived2 + player.PointsAdded2
        player.PointsGived3 = player.PointsGived3 + player.PointsAdded3
        player.PointsGived4 = player.PointsGived4 + player.PointsAdded4

        if player.PointsGived1 > group.get_player_by_id(1).payoff:
            player.PointsGived1 = group.get_player_by_id(1).payoff
        if player.PointsGived2 > group.get_player_by_id(2).payoff:
            player.PointsGived2 = group.get_player_by_id(2).payoff
        if player.PointsGived3 > group.get_player_by_id(3).payoff:
            player.PointsGived3 = group.get_player_by_id(3).payoff
        if player.PointsGived4 > group.get_player_by_id(4).payoff:
            player.PointsGived4 = group.get_player_by_id(4).payoff

        player.SubmittedOnce = True

        allocation_addition = [True, True, True, True]
        for p in group.get_players():
            my_id = p.id_in_group
            p.PointsReceived1 = getattr(group.get_player_by_id(1),f'PointsGived{my_id}')
            p.PointsReceived2 = getattr(group.get_player_by_id(2),f'PointsGived{my_id}')
            p.PointsReceived3 = getattr(group.get_player_by_id(3),f'PointsGived{my_id}')
            p.PointsReceived4 = getattr(group.get_player_by_id(4),f'PointsGived{my_id}')
            p.TotalReceived = p.PointsReceived1 + p.PointsReceived2 + p.PointsReceived3 + p.PointsReceived4
            TotalAllocationAdded = p.PointsAdded1 + p.PointsAdded2 + p.PointsAdded3 + p.PointsAdded4
            if TotalAllocationAdded == 0 and p.SubmittedOnce == True:
                allocation_addition[my_id-1] = False   
        if sum(allocation_addition) == 0:
            finished = True
        else:
            finished = False

        return {
            0: dict(finished=finished)
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        PlayerTotalAllocation = player.PointsGived1 + player.PointsGived2 + player.PointsGived3 + player.PointsGived4
        if PlayerTotalAllocation > 0:
            player.payoff = player.payoff -1 - player.PointsReceived1 - player.PointsReceived2 - player.PointsReceived3 - player.PointsReceived4 
        else:
            player.payoff = player.payoff - player.PointsReceived1 - player.PointsReceived2 - player.PointsReceived3 - player.PointsReceived4 
        if player.payoff < 0:
            player.payoff = 0

class Results(Page):
    timeout_seconds = 15

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        final_payoff_round = random.randint(1,C.NUM_ROUNDS)
        player.group.final_payoff_round = final_payoff_round

class FinalResults(Page):
    
    @staticmethod
    def vars_for_template(player: Player):
        final_payoff_round = player.group.final_payoff_round
        subsession_chosen = player.subsession.in_round(final_payoff_round)
        subsession_chosen_players = subsession_chosen.get_players()
        return {
            'subsession_chosen_players': subsession_chosen_players,
            'myself': player.in_round(final_payoff_round),
            'round_number': final_payoff_round
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
page_sequence = [Chat,Contribute, ContributionWaitPage, ContributionFeedback,AllocationStage1,AllocationStage1WaitPage,AllocationStage2,Results,FinalResults]
