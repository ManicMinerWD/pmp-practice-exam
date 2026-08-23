#!/usr/bin/env python3
import random
from collections import Counter

DOMAINS = {
  "P": "People (33%)",
  "R": "Process (41%)",
  "B": "Business Environment (26%)"
}

# Each: (domain, question, [o0,o1,o2,o3], correctIndex, explanation)
Q_raw = [
 # ---- PEOPLE (33%) — leadership, team, conflict, stakeholders, agile/hybrid ----
 ("P","A team member is consistently underperforming and others are covering for them. As the project manager, the MOST appropriate first action is to:",
  ["Have a private, supportive one-on-one to understand blockers and coach","Publicly criticize them in the standup","Reassign all their work immediately","Ignore it and let the team handle it"],0,
  "Address performance privately with empathy and coaching; servant leadership resolves root causes."),
 ("P","Two senior team members are in open conflict over technical approach. Your best action is to:",
  ["Facilitate a collaborative discussion to reach agreement on a solution","Pick one side immediately","Escalate to the sponsor at once","Let them fight it out"],0,
  "The PM facilitates conflict resolution collaboratively rather than dictating or avoiding."),
 ("P","A stakeholder is disengaged and missing key reviews. You should first:",
  ["Re-assess their needs and tailor communication to rebuild engagement","Remove them from the project","Send more generic emails","Ignore them"],0,
  "Re-engage through tailored communication and understanding their interests."),
 ("P","To build an effective team, the project manager should:",
  ["Establish a shared vision, ground rules, and psychological safety","Assign tasks with no context","Micromanage everyone","Avoid team meetings"],0,
  "High-performing teams need shared purpose, clear norms, and trust."),
 ("P","Servant leadership in an agile team means the PM:",
  ["Removes impediments and supports the team rather than directing them","Controls every decision","Assigns all tasks personally","Avoids the team"],0,
  "Servant leadership is about enabling the team, not commanding it."),
 ("P","A team is distributed across time zones. To keep them effective you should:",
  ["Agree on communication cadence, overlap hours, and async collaboration norms","Ignore the distance","Require all meetings at one timezone","Split them into silos"],0,
  "Virtual teams need deliberate communication and overlap planning."),
 ("P","Emotional intelligence helps the PM primarily by:",
  ["Reading team dynamics and managing own/others' emotions constructively","Memorizing formulas","Avoiding people","Writing reports"],0,
  "EI improves conflict, motivation, and collaboration."),
 ("P","A team member proposes a risky but innovative idea. You:",
  ["Encourage experimentation within safe-to-fail boundaries and learn","Shut it down immediately","Punish failure","Ignore it"],0,
  "Psychological safety encourages innovation; manage risk, don't kill ideas."),
 ("P","Stakeholders have conflicting priorities. You should:",
  ["Facilitate negotiation and align them to shared project objectives","Pick the loudest stakeholder","Ignore the conflict","Escalate instantly"],0,
  "Negotiation and alignment to objectives resolves stakeholder conflict."),
 ("P","To empower the team, the PM should:",
  ["Delegate decisions and build competence/confidence","Centralize all choices","Micromanage","Withhold information"],0,
  "Empowerment grows capability and ownership."),
 ("P","A new team lacks domain experience. Best approach:",
  ["Pair them with mentors and provide training/knowledge transfer","Replace them all","Ignore the gap","Blame them"],0,
  "Build capability via mentoring and training."),
 ("P","Team morale drops after a scope cut. You should:",
  ["Acknowledge the impact, re-explain the value, and re-engage the team","Pretend nothing changed","Punish low morale","Ignore it"],0,
  "Transparent leadership protects morale during change."),
 ("P","During a retrospective the team avoids honest feedback. You:",
  ["Model openness, normalize blameless retrospectives, and act on findings","Force blame","Skip retrospectives","Ignore feedback"],0,
  "Blameless retrospectives build continuous improvement."),
 ("P","A functional manager pulls your team member for other work. You:",
  ["Negotiate with the functional manager to protect needed capacity","Argue publicly","Do nothing","Reassign randomly"],0,
  "Resource conflicts are resolved by negotiation with resource owners."),
 ("P","The best way to manage a hybrid team's way of working is to:",
  ["Tailor ceremonies and controls to what each workstream needs","Force pure Scrum on everything","Force pure waterfall on everything","Avoid process"],0,
  "Hybrid delivery tailors approach per context."),
 ("P","A stakeholder keeps changing requirements mid-sprint. You:",
  ["Direct changes to the backlog and prioritize with the Product Owner","Allow silent mid-sprint changes","Refuse all changes","Ignore them"],0,
  "Changes belong in backlog grooming with the PO, not mid-iteration."),
 ("P","To improve collaboration with a resistant business unit you:",
  ["Involve them early and show how the project serves their goals","Exclude them","Criticize them","Dictate tasks"],0,
  "Early involvement and shared value reduce resistance."),
 ("P","The PM notices burnout signs in the team. The right action is to:",
  ["Address workload, protect sustainable pace, and remove impediments","Push harder for more output","Ignore it","Blame the team"],0,
  "Sustainable pace prevents burnout; servant leaders protect it."),
 ("P","Conflict between a developer and a tester about 'done' is best resolved by:",
  ["Agreeing a shared definition of done upfront","Letting them argue","Picking one side","Ignoring it"],0,
  "A clear DoD prevents recurring conflict."),
 ("P","A new stakeholder appears late and demands changes. You first:",
  ["Understand their interest and assess impact via change control","Implement immediately","Refuse","Ignore"],0,
  "Late changes go through change control after impact assessment."),
 ("P","To keep a virtual team cohesive you should:",
  ["Use visible boards, regular check-ins, and intentional relationship-building","Never meet","Work in silos","Avoid transparency"],0,
  "Visibility and connection sustain virtual teams."),
 ("P","A team member resists agile ceremonies as 'waste'. You:",
  ["Explain the purpose and adapt the ceremony to add value","Force compliance","Cancel all ceremonies","Ignore them"],0,
  "Adapt ceremonies to demonstrate value rather than mandate blindly."),
 ("P","The most effective way to handle a difficult conversation is to:",
  ["Focus on observable behavior and shared goals, not personality","Attack the person","Avoid it","Escalate immediately"],0,
  "Behavior- and goal-focused conversations are constructive."),
 ("P","You inherit a team with low trust. First step:",
  ["Demonstrate reliability and transparency to earn trust","Demand trust","Punish distrust","Ignore it"],0,
  "Trust is built through consistent, transparent behavior."),

 # ---- PROCESS (41%) — planning, execution, risk, quality, schedule, cost, procurement, agile/hybrid ----
 ("R","The MOST appropriate response when a key risk materializes is to:",
  ["Execute the agreed risk response and update the risk register","Panic","Ignore it","Blame the team"],0,
  "Planned responses are triggered; the register is updated."),
 ("R","A defect is found in a deliverable. You should first:",
  ["Contain it, log it, and follow the quality/issue process to root cause","Ship it anyway","Hide it","Blame someone"],0,
  "Defects are managed via quality and issue processes, not hidden."),
 ("R","The project is behind schedule. The BEST first action is to:",
  ["Analyze the critical path and re-plan with the team","Add people randomly","Cut scope without review","Ignore it"],0,
  "Schedule recovery starts with critical-path analysis and re-planning."),
 ("R","Earned value shows CPI = 0.85 and SPI = 0.90. This means:",
  ["Over budget and behind schedule","Under budget and ahead","On plan","No data"],0,
  "CPI<1 = over budget; SPI<1 = behind schedule."),
 ("R","A scope change is requested. You must:",
  ["Route it through change control and assess impact before approving","Implement immediately","Refuse always","Ignore"],0,
  "All changes go through integrated change control."),
 ("R","To select the right delivery approach you should:",
  ["Match predictive/agile/hybrid to the work's uncertainty and context","Always use waterfall","Always use Scrum","Pick randomly"],0,
  "Tailoring the approach fits the context."),
 ("R","A sprint goal is at risk. The team should:",
  ["Swarm on the highest-priority items and protect the goal","Add unrelated work","Abandon the sprint","Ignore the risk"],0,
  "The team focuses on the sprint goal; the PO may descope."),
 ("R","A vendor misses a milestone. Your action:",
  ["Review the contract/SLA, communicate impact, and pursue corrective action","Terminate instantly","Ignore it","Blame them"],0,
  "Procurement issues use the contract and corrective action."),
 ("R","Quality is best ensured by:",
  ["Building quality in via standards and continuous verification, not inspection alone","Inspecting only at the end","Skipping tests","Assuming it's fine"],0,
  "Prevention and built-in quality beat end inspection."),
 ("R","A stakeholder wants daily detailed reports. You should:",
  ["Agree a communication plan matching their need and value","Send everything hourly","Refuse","Ignore"],0,
  "Communication is planned to stakeholder needs."),
 ("R","The project's requirements are unclear. Best approach:",
  ["Use an adaptive approach with incremental refinement and feedback","Fix a full plan upfront","Guess","Ignore"],0,
  "High uncertainty favors adaptive, iterative refinement."),
 ("R","To manage a portfolio of risks you use:",
  ["A risk register with probability/impact and owned responses","Memory alone","No tracking","Blame"],0,
  "Risks are tracked and owned in the register."),
 ("R","A major dependency is delayed by another project. You:",
  ["Coordinate with that project's PM and adjust the schedule/sequence","Blame them","Do nothing","Escalate instantly"],0,
  "Cross-project dependencies need coordination."),
 ("R","The team recommends automating a manual test. You:",
  ["Evaluate cost/benefit and adopt if it improves quality and flow","Reject reflexively","Ignore","Force it"],0,
  "Decisions weigh value and impact."),
 ("R","During execution, a new law affects the design. You:",
  ["Assess impact, route through change control, and update the plan","Ignore the law","Implement without review","Blame the sponsor"],0,
  "External changes trigger change control and re-planning."),
 ("R","A task is taking longer than estimated. The PM should:",
  ["Check for impediments and help the team remove them","Punish the team","Ignore","Re-estimate blindly"],0,
  "Servant leaders remove impediments causing delays."),
 ("R","To control the budget you should:",
  ["Monitor actuals vs plan, forecast, and act on variances","Ignore spend","Cut quality to save cost","Guess"],0,
  "Cost control uses monitoring and forecasting."),
 ("R","A retrospective identifies a process problem. Next:",
  ["Agree a concrete improvement and try it next iteration","Debate forever","Ignore","Blame"],0,
  "Retrospectives produce actionable improvements."),
 ("R","The sponsor asks for a status you don't have. You:",
  ["Get the data from the team/tooling and report transparently","Invent numbers","Guess","Refuse"],0,
  "Report on real data, not assumptions."),
 ("R","A requirement conflicts with a compliance rule. You:",
  ["Surface the conflict and resolve with stakeholders before proceeding","Proceed anyway","Ignore compliance","Hide it"],0,
  "Compliance conflicts must be resolved, not bypassed."),
 ("R","To close the project you should:",
  ["Confirm objectives met, hand over, capture lessons learned, and release resources","Disappear","Skip handover","Ignore lessons"],0,
  "Closure includes handover, lessons, and release."),
 ("R","Work is falling into a bottleneck. You apply:",
  ["Flow analysis (e.g., WIP limits) to relieve the constraint","Add more reports","Ignore","Blame"],0,
  "Bottlenecks are managed with flow/WIP techniques."),
 ("R","The Product Owner reprioritizes the backlog. As PM you:",
  ["Support it and help the team re-plan the next iteration","Refuse","Ignore","Dictate order"],0,
  "Backlog priority is the PO's call; the PM supports delivery."),
 ("R","A spike is needed to reduce technical uncertainty. You:",
  ["Time-box a short experiment to learn, then decide","Guess indefinitely","Ignore","Blame"],0,
  "Spikes are time-boxed learning to cut uncertainty."),
 ("R","Stakeholders disagree on success criteria. You:",
  ["Facilitate agreement on measurable acceptance criteria","Pick yours","Ignore","Escalate instantly"],0,
  "Clear acceptance criteria prevent disputes."),
 ("R","A resource is over-allocated across two projects. You:",
  ["Negotiate leveling with the resource managers","Overload them","Ignore","Blame"],0,
  "Over-allocation is resolved by negotiation/leveling."),
 ("R","To keep execution transparent you use:",
  ["A visible board and regular demos/reviews","Secret tracking","No updates","Guesswork"],0,
  "Transparency via boards and demos builds trust."),
 ("R","An issue is escalating beyond the team. You:",
  ["Log it, assess, and escalate with options to the right level","Hide it","Blame","Ignore"],0,
  "Issues are logged and escalated with context."),

 # ---- BUSINESS ENVIRONMENT (26%) — strategy, benefits, compliance, change, AI, sustainability ----
 ("B","A project's business case is no longer valid. You should:",
  ["Flag it to sponsors and recommend reconsideration or closure","Keep going silently","Hide the issue","Blame the team"],0,
  "Loss of business justification must be escalated."),
 ("B","Benefits realization is the PM's concern because:",
  ["Projects exist to deliver outcomes/benefits, not just outputs","Outputs are enough","Benefits are optional","Ignore value"],0,
  "Value, not deliverables alone, justifies the project."),
 ("B","Outputs, outcomes, and benefits differ in that:",
  ["Outputs are deliverables; outcomes are changes from them; benefits are the value gained","They are the same","Only outputs matter","Benefits are outputs"],0,
  "Understanding the chain keeps focus on value."),
 ("B","A new regulation affects the project. You must:",
  ["Identify the compliance need and ensure the project meets it","Ignore the law","Proceed anyway","Hide it"],0,
  "Compliance is non-negotiable; assess and meet it."),
 ("B","The organization is undergoing change. You support it by:",
  ["Communicating, training, and sustaining adoption after go-live","Ignoring resistance","Forcing change","Hiding impacts"],0,
  "Change management sustains adoption."),
 ("B","A project conflicts with organizational strategy. You:",
  ["Realign it to strategy or raise the mismatch to sponsors","Ignore strategy","Proceed","Blame"],0,
  "Projects must serve strategy."),
 ("B","Enterprise environmental factors influence the project by:",
  ["Shaping constraints/options (market, law, culture) you must work within","Being irrelevant","Only helping","Never mattering"],0,
  "EEFs are external realities affecting choices."),
 ("B","Organizational process assets help by:",
  ["Providing templates, lessons, and standards to reuse","Being ignored","Slowing you","Harming"],0,
  "OPAs are reusable internal knowledge."),
 ("B","AI tooling is introduced to the project. Best practice:",
  ["Use it to augment analysis with human oversight and accountability","Replace all judgment blindly","Ban it","Ignore risks"],0,
  "AI augments; humans stay accountable (new 2026 BE topic)."),
 ("B","Sustainability is part of delivery when:",
  ["The project considers environmental/social impact in choices","It never matters","Only cost matters","Ignore it"],0,
  "Sustainable delivery is a 2026 BE emphasis."),
 ("B","Knowledge transfer at closure ensures:",
  ["Lessons and know-how pass to the organization for continuity","It is skipped","Hidden","Lost"],0,
  "Knowledge transfer enables continuity."),
 ("B","A project delivers but users won't adopt it. Likely cause:",
  ["Insufficient change management and stakeholder engagement","Good training","Clear value","Strong comms"],0,
  "Adoption failure usually means weak change management."),
 ("B","To demonstrate value to executives you:",
  ["Show benefits realized against the business case with metrics","Show only tasks done","Hide results","Guess"],0,
  "Value is shown with measured benefits."),
 ("B","External market shift threatens project relevance. You:",
  ["Reassess and recommend pivoting, pausing, or stopping","Ignore it","Proceed blindly","Blame"],0,
  "Environmental change requires reassessment."),
 ("B","Governance requires stage approvals. You:",
  ["Present status and a recommendation at each gate","Skip gates","Hide bad news","Guess"],0,
  "Stage gates need transparent recommendations."),
 ("B","A benefits owner is needed because:",
  ["Someone must track and realize benefits after delivery","No one cares","Benefits are automatic","Ignore"],0,
  "Benefits need an accountable owner post-delivery."),
 ("B","Compliance evidence should be:",
  ["Maintained and auditable throughout the project","Ignored","Faked","Deleted"],0,
  "Audit-ready compliance evidence is essential."),
 ("B","The PM supports strategy by:",
  ["Selecting work that advances prioritized organizational objectives","Doing random work","Ignoring goals","Blame"],0,
  "Delivery should advance strategy."),
 ("B","Resistance to a project is best handled by:",
  ["Understanding concerns and co-creating the change with those affected","Forcing it","Ignoring","Blaming"],0,
  "Co-creation reduces resistance."),
 ("B","To keep the project aligned to value you regularly:",
  ["Revisit the business case and benefits with sponsors","Never revisit","Hide drift","Guess"],0,
  "Periodic business-case review maintains alignment."),
]

# robust count fix: trim or pad to exactly 70
print("raw count:", len(Q_raw), "domains:", dict(Counter(q[0] for q in Q_raw)))
while len(Q_raw) > 70:
    for i in range(len(Q_raw)-1, -1, -1):
        if Q_raw[i][0] == "B":
            del Q_raw[i]; break
while len(Q_raw) < 70:
    Q_raw.append(("P","A team member excels but feels unrecognized. You:",
      ["Recognize their contribution specifically and publicly (appropriately)","Ignore them","Criticize","Reassign"],0,
      "Recognition sustains engagement."))

# balance correct positions A/B/C/D
random.seed(731)  # PMP seed
random.seed(2026)
targets = [0,1,2,3] * (70//4)
while len(targets) < 70:
    targets.append(len(targets) % 4)
random.shuffle(targets)
Q = []
for i,(dom,q,opts,ai,exp) in enumerate(Q_raw):
    t = targets[i]
    shift = (ai - t) % len(opts)
    rotd = opts[shift:] + opts[:shift]
    Q.append({"d":dom,"q":q,"o":rotd,"a":t,"x":exp})
dist = [0,0,0,0]
for q in Q: dist[q["a"]] += 1
for i,(dom,q,opts,ai,exp) in enumerate(Q_raw):
    assert Q[i]["o"][Q[i]["a"]] == opts[ai], "integrity fail at %d" % i
print("final:", len(Q), "domains:", dict(Counter(q["d"] for q in Q)), "dist:", dist, "INTEGRITY OK")

# ---------------- HTML builder (fixed: reveal only on click) ----------------
def jss(s): return s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")
STUDYGUIDE = {
  "P":["Lead with servant leadership: enable the team, resolve conflict collaboratively.","Build trust, psychological safety, and clear ground rules.","Engage stakeholders via tailored communication; ~60% of the exam is agile/hybrid."],
  "R":["Master change control, risk responses, EVM (CPI/SPI), and quality built-in.","Tailor predictive/agile/hybrid to context; protect the sprint/iteration goal.","Track issues, dependencies, and cost/schedule variances transparently."],
  "B":["Projects exist for benefits/value — keep the business case alive.","Meet compliance; support change management and adoption.","New 2026 topics: AI augmentation with human oversight, sustainability, value delivery."]
}
Q_json = "[\n" + ",\n".join(
    '  {d:"%s",q:"%s",o:["%s","%s","%s","%s"],a:%d,x:"%s"}' % (
        q["d"], jss(q["q"]), jss(q["o"][0]), jss(q["o"][1]), jss(q["o"][2]), jss(q["o"][3]), q["a"], jss(q["x"])
    ) for q in Q
) + "\n]"
DOM_json = "{" + ",".join('"%s":"%s"' % (k, jss(v)) for k,v in DOMAINS.items()) + "}"
SG_json = "{" + ",".join('"%s":["%s"]' % (k, '","'.join(jss(s) for s in v)) for k,v in STUDYGUIDE.items()) + "}"

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PMP Practice Exam</title>
<style>
:root{--bg:#0b1020;--card:#151c2e;--fg:#e8ecf5;--muted:#9aa6c0;--accent:#6ea8fe;--good:#3ecf8e;--bad:#ff6b6b;--line:#26304a}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);line-height:1.5}
header{padding:18px 22px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;align-items:center;gap:12px}
header h1{font-size:1.15rem;margin:0;font-weight:650}
.pill{background:#1d2742;border:1px solid var(--line);color:var(--muted);padding:3px 10px;border-radius:999px;font-size:.78rem}
.spacer{flex:1}
button{cursor:pointer;border:1px solid var(--line);background:#1b2540;color:var(--fg);padding:9px 16px;border-radius:8px;font-size:.92rem;transition:.15s}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);color:#08101f;border-color:var(--accent);font-weight:600}
button:disabled{opacity:.45;cursor:not-allowed}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:14px 22px;border-bottom:1px solid var(--line)}
.modebtns button.active{background:var(--accent);color:#08101f;border-color:var(--accent)}
#timer{font-variant-numeric:tabular-nums;color:var(--muted);font-size:.9rem}
main{padding:22px;max-width:820px;margin:0 auto}
#quiz{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px}
.qhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;gap:10px}
.qdomain{font-size:.74rem;color:var(--accent);text-transform:uppercase;letter-spacing:.04em}
.qno{font-size:.8rem;color:var(--muted)}
.question{font-size:1.05rem;margin-bottom:18px;font-weight:550}
.options{display:flex;flex-direction:column;gap:10px}
.opt{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid var(--line);border-radius:9px;background:#121a2e;transition:.12s}
.opt:hover{border-color:var(--accent)}
.opt input{accent-color:var(--accent);width:17px;height:17px}
.opt.correct{border-color:var(--good);background:rgba(62,207,142,.12)}
.opt.wrong{border-color:var(--bad);background:rgba(255,107,107,.12)}
.opt.dim{opacity:.55}
.exp{margin-top:16px;padding:13px 15px;border-left:3px solid var(--accent);background:#101a30;border-radius:6px;font-size:.92rem;color:#cdd6ea}
.qnav{display:flex;justify-content:space-between;align-items:center;margin-top:20px;gap:10px}
.qcontrols{display:flex;gap:10px}
.score{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px;margin-top:22px;display:none}
.score h2{margin-top:0}
.big{font-size:2.4rem;font-weight:700;margin:6px 0}
.legend{font-size:.85rem;color:var(--muted);margin-top:8px}
#pie{display:flex;flex-direction:column;align-items:center;margin:16px 0}
#pie svg{max-width:240px}
.pielabel{font-size:.8rem;color:var(--muted);text-align:center;margin-top:4px}
.break{display:flex;flex-direction:column;gap:9px;margin-top:16px}
.brow{display:flex;justify-content:space-between;gap:12px;font-size:.9rem;padding:9px 12px;background:#121a2e;border:1px solid var(--line);border-radius:8px}
.brow .pct{font-weight:650}
.rec{margin-top:18px;padding:16px;border:1px solid var(--good);border-radius:10px;background:rgba(62,207,142,.08);display:none}
.rec h3{margin:0 0 8px;font-size:1rem}
.rec ul{margin:6px 0 0;padding-left:20px;font-size:.9rem;color:#cdd6ea}
#review{margin-top:20px}
.review-item{padding:13px 15px;border:1px solid var(--line);border-radius:9px;margin-bottom:10px;background:#121a2e}
.review-item .rq{font-weight:550;margin-bottom:6px}
.review-item .rr{font-size:.85rem}
.review-item .ok{color:var(--good)}
.review-item .no{color:var(--bad)}
.review-item .rx{font-size:.84rem;color:#cdd6ea;margin-top:6px}
footer{padding:18px 22px;color:var(--muted);font-size:.78rem;border-top:1px solid var(--line);margin-top:30px}
a{color:var(--accent)}
</style></head>
<body>
<header>
  <h1>PMP Practice Exam</h1>
  <span class="pill">Project Management Professional (PMI)</span>
  <span class="pill">70 questions</span>
  <span class="spacer"></span>
  <span id="progress" class="pill">Answered 0 / 70</span>
</header>

<div class="toolbar">
  <div class="modebtns">
    <button id="btnStudy" class="active" onclick="setMode('study')">Study mode</button>
    <button id="btnExam" onclick="setMode('exam')">Exam mode</button>
  </div>
  <span id="timer"></span>
  <span class="spacer"></span>
  <button id="endBtn" class="primary" onclick="endExam()">End exam</button>
  <button onclick="resetExam()">Reset</button>
</div>

<main>
  <div id="quiz"></div>
  <div class="score" id="score">
    <h2>Result</h2>
    <div class="big"><span id="scnum">0</span><span style="font-size:1rem;color:var(--muted)"> / 70</span></div>
    <div id="verdict" class="legend"></div>
    <div id="pie"></div>
    <div class="break" id="breakdown"></div>
    <div class="rec" id="rec"><h3>Focus area — weakest domain</h3><ul id="recul"></ul></div>
    <div id="review"></div>
  </div>
</main>

<footer>
  Self-made study companion for the PMI PMP exam using the 2026 Exam Content Outline (ECO). Not an official PMI product.
  Real exam: 180 questions (170 scored), 240 minutes, ~70% to pass. Pair with the official <a href="https://www.pmi.org/certifications/project-management-pmp" target="_blank">PMP</a> resources and ECO.
</footer>

<script>
const DOMAINS = __DOM__;
const STUDYGUIDE = __SG__;
const Q = __Q__;
const EXAM_MINUTES = 240;
const PASS_PCT = 70;

let mode = 'study';
let current = 0;
const answers = new Array(Q.length).fill(null);
const revealed = new Array(Q.length).fill(false);
let timer = null, remaining = EXAM_MINUTES*60;
const quiz = document.getElementById('quiz');

function setMode(m){
  mode = m;
  document.getElementById('btnStudy').classList.toggle('active', m==='study');
  document.getElementById('btnExam').classList.toggle('active', m==='exam');
  document.getElementById('timer').style.visibility = (m==='exam') ? 'visible':'hidden';
  if(m==='exam'){ startTimer(); } else { stopTimer(); document.getElementById('timer').textContent=''; }
  renderCurrent();
}
function startTimer(){
  stopTimer();
  remaining = EXAM_MINUTES*60;
  updateTimer();
  timer = setInterval(()=>{ remaining--; updateTimer(); if(remaining<=0){ stopTimer(); endExam(); } },1000);
}
function stopTimer(){ if(timer){ clearInterval(timer); timer=null; } }
function updateTimer(){
  const m=Math.floor(remaining/60), s=remaining%60;
  document.getElementById('timer').textContent='Time '+m+':'+(s<10?'0':'')+s;
}
function updateProgress(){
  const n=answers.filter(a=>a!==null).length;
  document.getElementById('progress').textContent='Answered '+n+' / '+Q.length;
}
function renderCurrent(){
  const q=Q[current];
  let hs='<div class="qhead"><span class="qdomain">'+DOMAINS[q.d]+'</span><span class="qno">Question '+(current+1)+' of '+Q.length+'</span></div>';
  hs+='<div class="question">'+q.q+'</div><div class="options">';
  const chosen=answers[current];
  const show=revealed[current];
  q.o.forEach((opt,i)=>{
    let cls='opt';
    if(show){
      if(i===q.a) cls+=' correct';
      else if(chosen===i) cls+=' wrong';
      else cls+=' dim';
    }
    hs+='<label class="'+cls+'"><input type="radio" name="opt" value="'+i+'" '+(chosen===i?'checked':'')+' onchange="choose('+i+')"> '+opt+'</label>';
  });
  hs+='</div>';
  if(show){ hs+='<div class="exp"><strong>Explanation:</strong> '+q.x+'</div>'; }
  const last = current===Q.length-1;
  hs+='<div class="qnav"><button onclick="go(-1)" '+(current===0?'disabled':'')+'>&larr; Back</button>';
  hs+='<div class="qcontrols">';
  if(mode==='study' && !revealed[current]) hs+='<button onclick="reveal()">Reveal answer</button>';
  hs+='<button class="primary" onclick="go(1)">'+(last?'Review / End':'Next &rarr;')+'</button>';
  hs+='</div></div>';
  quiz.innerHTML=hs;
}
function choose(i){ answers[current]=i; updateProgress(); renderCurrent(); }
function reveal(){ revealed[current]=true; renderCurrent(); }
function go(dir){
  const nxt=current+dir;
  if(nxt<0) return;
  if(nxt>=Q.length){ endExam(); return; }
  current=nxt; renderCurrent();
}
function endExam(){
  stopTimer();
  const answered=answers.filter(a=>a!==null).length;
  let correct=0; const dom={};
  Object.keys(DOMAINS).forEach(k=>dom[k]={t:0,c:0});
  Q.forEach((q,i)=>{ dom[q.d].t++; if(answers[i]===q.a){ correct++; dom[q.d].c++; } });
  const pct=Math.round(correct/Q.length*100);
  document.getElementById('scnum').textContent=correct;
  const pass = pct>=PASS_PCT;
  document.getElementById('verdict').textContent = 'You answered '+answered+' of '+Q.length+'. Score: '+pct+'% — '+(pass?'PASS (≥'+PASS_PCT+'%)':'BELOW PASS (≥'+PASS_PCT+'%)');
  renderPie(dom,pct);
  const bd=document.getElementById('breakdown'); bd.innerHTML='';
  Object.keys(DOMAINS).forEach(k=>{
    const d=dom[k]; const p=d.t?Math.round(d.c/d.t*100):0;
    const cls = p>=PASS_PCT?'ok':'no';
    bd.innerHTML+='<div class="brow"><span>'+DOMAINS[k]+' <span style="color:var(--muted)">('+d.t+' Q)</span></span><span class="pct '+cls+'">'+d.c+'/'+d.t+' · '+p+'%</span></div>';
  });
  const rec=document.getElementById('rec'); rec.classList.add('show');
  const weakest=Object.keys(DOMAINS).map(k=>({k,p:dom[k].t?dom[k].c/dom[k].t:1})).sort((a,b)=>a.p-b.p)[0];
  const ul=document.getElementById('recul'); ul.innerHTML='';
  (STUDYGUIDE[weakest.k]||[]).forEach(t=>ul.innerHTML+='<li>'+t+'</li>');
  const rv=document.getElementById('review'); rv.innerHTML='<h3 style="margin:18px 0 8px">Review</h3>';
  Q.forEach((q,i)=>{
    const ok=answers[i]===q.a;
    rv.innerHTML+='<div class="review-item"><div class="rq">'+(i+1)+'. '+q.q+'</div>'+
      '<div class="rr '+(ok?'ok':'no')+'">'+(ok?'✓ Correct':'✗ Your answer: '+(answers[i]!==null?q.o[answers[i]]:'—'))+' &nbsp;|&nbsp; Correct: '+q.o[q.a]+'</div>'+
      '<div class="rx"><strong>Why:</strong> '+q.x+'</div></div>';
  });
  document.getElementById('score').style.display='block';
  document.getElementById('score').scrollIntoView({behavior:'smooth'});
}
function renderPie(dom, pct){
  const colors={P:'#6ea8fe',R:'#3ecf8e',B:'#f5a623'};
  const segs=Object.keys(DOMAINS);
  const total=segs.reduce((s,k)=>s+dom[k].t,0);
  const R=70,Cx=90,Cy=90,sw=26;
  let off=0,paths='';
  segs.forEach(k=>{
    const frac=dom[k].t/total, len=frac*2*Math.PI*R, col=colors[k]||'#888';
    paths+='<circle cx="'+Cx+'" cy="'+Cy+'" r="'+R+'" fill="none" stroke="'+col+'" stroke-width="'+sw+'" '+
      'stroke-dasharray="'+len+' '+(2*Math.PI*R-len)+'" stroke-dashoffset="'+(-off)+'" transform="rotate(-90 '+Cx+' '+Cy+')"></circle>';
    off+=len;
  });
  document.getElementById('pie').innerHTML=
    '<svg viewBox="0 0 180 180" width="200" height="200">'+paths+
    '<text x="90" y="84" text-anchor="middle" font-size="26" font-weight="700" fill="#e8ecf5">'+pct+'%</text>'+
    '<text x="90" y="104" text-anchor="middle" font-size="11" fill="#9aa6c0">correct</text></svg>'+
    '<div class="pielabel">Segments sized by question count per domain</div>';
}
function resetExam(){
  for(let i=0;i<Q.length;i++){answers[i]=null; revealed[i]=false;}
  current=0; document.getElementById('score').style.display='none';
  if(mode==='exam') startTimer(); updateProgress(); renderCurrent();
}
setMode('study');
updateProgress();
</script>
</body></html>
"""
html = html.replace("__DOM__", DOM_json).replace("__SG__", SG_json).replace("__Q__", Q_json)
open("/Users/warrenduncan/pmp-practice-exam/index.html","w").write(html)
print("written", len(html), "bytes")
