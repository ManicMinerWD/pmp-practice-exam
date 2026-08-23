#!/usr/bin/env python3
import random
from collections import Counter
from _bal import balance

DOMAINS = {
  "P": "People (33%)",
  "R": "Process (41%)",
  "B": "Business Environment (26%)"
}

# Each tuple is ONE line: (domain, question, o0, o1, o2, o3, correctIndex, explanation)
# All four options are full, plausible statements of comparable length so the correct
# answer cannot be identified by length. The correct option index is marked.
Q_raw = [
 # ===== PEOPLE (33%) — 50 =====
 ("P","A team member is consistently underperforming and others are covering for them. As the project manager, the MOST appropriate first action is to:","Have a private, supportive one-on-one to understand blockers and coach the person","Publicly compare their output to the top performer to create pressure","Reassign all of their work to others immediately without discussion","Document the issue and begin formal termination steps at once",0,"Address performance privately with empathy and coaching; servant leadership resolves root causes."),
 ("P","Two senior team members are in open conflict over technical approach. Your best action is to:","Facilitate a collaborative discussion to reach agreement on a solution","Pick one side immediately so the team can move on","Escalate to the sponsor before either person has spoken","Let them fight it out until one concedes defeat",0,"The PM facilitates conflict resolution collaboratively rather than dictating or avoiding."),
 ("P","A stakeholder is disengaged and missing key reviews. You should first:","Re-assess their needs and tailor communication to rebuild engagement","Remove them from the project's stakeholder register entirely","Send more of the same generic status emails each week","Stop inviting them and note the gap in the issue log",0,"Re-engage through tailored communication and understanding their interests."),
 ("P","To build an effective team, the project manager should:","Establish a shared vision, ground rules, and psychological safety","Assign tasks with no context so people stay flexible","Micromanage everyone to guarantee consistent output","Avoid team meetings to maximize individual focus time",0,"High-performing teams need shared purpose, clear norms, and trust."),
 ("P","Servant leadership in an agile team means the PM:","Removes impediments and supports the team rather than directing them","Controls every decision to keep the plan on track","Assigns all tasks personally and checks them daily","Avoids the team so they learn to be self-sufficient",0,"Servant leadership is about enabling the team, not commanding it."),
 ("P","A team is distributed across time zones. To keep them effective you should:","Agree on communication cadence, overlap hours, and async collaboration norms","Ignore the distance since tools make it irrelevant","Require all meetings at the PM's own time zone only","Split them into separate silos that never coordinate",0,"Virtual teams need deliberate communication and overlap planning."),
 ("P","Emotional intelligence helps the PM primarily by:","Reading team dynamics and managing own and others' emotions constructively","Memorizing formulas for the schedule and cost baselines","Avoiding people so that conflict never arises","Writing longer status reports for leadership",0,"EI improves conflict, motivation, and collaboration."),
 ("P","A new team member feels excluded from decisions. You should:","Invite their input early and clarify how decisions are made","Tell them to wait until they have earned trust","Keep them on administrative tasks only for six months","Ask the team to vote them out if they underperform",0,"Inclusion builds ownership and psychological safety."),
 ("P","The project team disagrees on the definition of done. The PM should:","Facilitate agreement on a shared, documented definition of done","Impose the PM's own definition without debate","Use a different definition for each workstream","Skip the definition and review at release only",0,"A shared DoD aligns quality expectations across the team."),
 ("P","A team member raises an ethical concern about a suggested shortcut. You should:","Hear the concern, review the policy, and choose the compliant path","Tell them to follow the instruction to keep the schedule","Report them to HR for refusing a direct task","Ignore it because the sponsor approved the work",0,"Ethical concerns must be addressed against the code of conduct."),
 ("P","To improve team performance you should first:","Identify the root cause with the team before changing process","Replace the lowest performer on the next rotation","Increase oversight and status meeting frequency","Benchmark salaries against the market immediately",0,"Root-cause analysis with the team prevents recurring issues."),
 ("P","A senior stakeholder demands a change that conflicts with team values. You should:","Discuss the impact, explore options, and reach a principled compromise","Implement it exactly to avoid disappointing the stakeholder","Refuse outright and escalate to the steering committee","Quietly drop it and hope no one notices the gap",0,"Negotiate on principle while preserving the relationship."),
 ("P","The PM notices low morale after a missed milestone. Best response is to:","Hold a frank retro, acknowledge the miss, and reset with the team","Blame the vendor publicly to protect the team","Hide the miss from the team to avoid panic","Tighten controls and add daily status meetings",0,"Honest retros build trust and surface improvement actions."),
 ("P","A conflict arises between a functional manager and the project team. You should:","Clarify roles, shared goals, and negotiate a working agreement","Defer all decisions to the functional manager","Remove the team from the functional manager's oversight","Escalate immediately to the program office",0,"Matrix conflicts need clarified roles and shared goals."),
 ("P","To develop team members you should:","Agree on growth goals and provide coaching and stretch assignments","Keep them on the same tasks to build deep routine","Rotate them off the project if they slow down","Limit training to mandatory compliance courses",0,"Coaching and stretch work develop capability and engagement."),
 ("P","A virtual team struggles with trust. You should:","Create opportunities for informal interaction and consistent follow-through","Require cameras on for every meeting as punishment","Replace remote members with local staff","Reduce communication to written status only",0,"Trust grows from interaction and reliable behavior."),
 ("P","Stakeholder engagement is best sustained by:","A tailored engagement plan with two-way communication","A monthly generic newsletter to all parties","Contacting only when something goes wrong","Limiting access to protect the team's focus",0,"Planned, two-way engagement maintains support."),
 ("P","The PM learns a team member is overworked and at risk of burnout. You should:","Rebalance the workload and check capacity with the team","Praise their dedication and ask for more output","Reassign their work to someone else silently","Note it in the risk register and move on",0,"Sustainable pace protects delivery and well-being."),
 ("P","A disagreement on priorities emerges between two product owners. You should:","Facilitate prioritization against value and agreed criteria","Let the most senior person decide unilaterally","Freeze all work until they agree","Pick the cheaper item to reduce risk",0,"Prioritization needs transparent value-based criteria."),
 ("P","The team resists a new mandated tool. Best approach is to:","Explain the why, involve them in rollout, and address concerns","Mandate use and track compliance strictly","Abandon the tool to keep peace","Punish early resisters publicly",0,"Change is adopted through involvement and clear purpose."),
 ("P","A PM inherits a divided team. First step is to:","Listen to individuals, map dynamics, and build a shared purpose","Reorganize reporting lines on day one","Replace half the team immediately","Avoid team sessions to reduce tension",0,"Understanding precedes restructuring."),
 ("P","To handle a high-performing but arrogant contributor you should:","Give candid feedback and channel their strength to team goals","Promote them above the team to use the confidence","Isolate them from collaboration tasks","Ignore the behavior to avoid conflict",0,"Candid feedback redirects strength productively."),
 ("P","Stakeholders are surprised by a delay they should have seen. The gap is:","Insufficient proactive communication and expectation setting","A lack of technical skill on the team","Poor vendor contract language only","The sponsor's absence from kickoff",0,"Surprise indicates a communication-plan failure."),
 ("P","The PM wants to empower the team. Effective action is to:","Delegate decisions and create safety for them to act","Centralize all decisions to reduce errors","Approve every task before it starts","Limit their contact with stakeholders",0,"Empowerment requires delegated authority and safety."),
 ("P","A team member declines a task citing a conflict of interest. You should:","Thank them, reassign the task, and note the disclosure","Force them to proceed to avoid delay","Report them for insubordination","Ignore the conflict and assign it anyway",0,"Disclosed conflicts must be respected and managed."),
 ("P","During a retrospective the team avoids hard topics. You should:","Set a safe frame, use data, and model openness yourself","Skip the retro and keep shipping","Name and shame the quietest member","Let the sponsor run the session instead",0,"Psychological safety enables honest retros."),
 ("P","A new stakeholder joins mid-project with strong views. You should:","Onboard them, share context, and integrate their input","Defer to them on all decisions immediately","Exclude them until the next phase","Challenge their credentials in the meeting",0,"Onboarding protects continuity and buy-in."),
 ("P","The team is highly dependent on one expert. To reduce risk you should:","Encourage knowledge sharing and cross-training deliberately","Keep the expert isolated to preserve speed","Document only what the expert allows","Hire a second expert at double cost",0,"Cross-training reduces single-points-of-failure."),
 ("P","Motivation drops after a long stretch of crunch. You should:","Restore sustainable pace and reconnect work to purpose","Extend the crunch until the release ships","Offer a one-time bonus and move on","Reduce feedback to avoid discomfort",0,"Recovery and purpose rebuild motivation."),
 ("P","A peer PM asks you to falsify a status report. You should:","Decline, explain the policy, and offer to show the real data","Agree to protect the working relationship","Falsify only the schedule not the budget","Forward the request to the sponsor anonymously",0,"Integrity requires accurate reporting."),
 ("P","To resolve a persistent personality clash you should:","Focus on interests and the work, not personalities","Assign them to opposite shifts permanently","Move one to another project without discussion","Ask the team to vote one out",0,"Interest-based resolution depersonalizes conflict."),
 ("P","The project sponsor is unavailable and decisions stall. You should:","Use the agreed delegation of authority and escalate per the plan","Wait silently until the sponsor returns","Make large scope cuts on your own","Bypass the sponsor and ask the CEO",0,"Defined authority keeps work moving."),
 ("P","A team member wants to use a new technique you doubt. You should:","Agree a small safe experiment and review the result together","Forbid it to avoid risk entirely","Approve it fully without oversight","Mock the idea in the standup",0,"Safe-to-fail experiments enable learning."),
 ("P","Trust with the sponsor is weak. You should:","Be consistent, transparent, and deliver on small commitments","Overpromise to impress them quickly","Communicate only good news","Avoid them to reduce friction",0,"Trust is built through consistent, honest delivery."),
 ("P","The team misses commitments repeatedly. Root cause is likely:","Unrealistic planning or unclear scope, not laziness","A lazy team that should be replaced","Poor tools that must be upgraded","Insufficient daily meetings",0,"Systemic causes beat blame."),
 ("P","A junior member makes a costly mistake. You should:","Treat it as a learning event, fix the process, and coach","Discipline them formally in writing","Reassign all their work permanently","Hide it from the sponsor",0,"Blame-free learning improves the system."),
 ("P","Stakeholder power shifts mid-project. You should:","Re-assess the engagement plan and adjust influence strategies","Keep the old plan unchanged","Ignore the new stakeholder","Remove the old stakeholder",0,"Engagement plans must track power changes."),
 ("P","The PM is asked to fast-track by skipping reviews. You should:","Weigh the risk, add lighter checkpoints, and get informed sign-off","Skip all reviews to save time","Refuse and stop the work","Add more reviews than before",0,"Fast-tracking needs managed risk, not abandoned control."),
 ("P","A team member excels but wants advancement. You should:","Discuss a development path and sponsor stretch opportunities","Promise a promotion you cannot give","Keep them static to retain them","Suggest they leave for growth",0,"Development paths retain and grow talent."),
 ("P","Conflict between delivery speed and quality arises. You should:","Facilitate a trade-off discussion with explicit acceptance criteria","Always choose speed to please the sponsor","Always choose quality regardless of cost","Flip a coin to decide",0,"Trade-offs need explicit, agreed criteria."),
 ("P","The PM observes a pattern of silent disagreements. You should:","Create explicit forums for dissent and decision records","Assume silence means agreement","Punish disagreement publicly","Make all decisions yourself",0,"Dissent surfaced early prevents late failure."),
 ("P","A stakeholder disputes a requirement you finalized. You should:","Re-open the traceability and confirm the source of the need","Defend the document rigidly","Change it without checking impact","Remove the requirement entirely",0,"Requirements tie back to validated needs."),
 ("P","The team is resistant to estimates. You should:","Explain the purpose, use relative sizing, and let them own numbers","Impose fixed dates from management","Stop estimating and guess","Estimate for them in private",0,"Owned estimates are more reliable."),
 ("P","You inherit a project with no charter. First action is to:","Collaborate to create a charter that clarifies purpose and authority","Start executing tasks to show progress","Wait for the sponsor to send one","Rewrite the old plan from memory",0,"A charter establishes mandate and alignment."),
 ("P","A senior team lead undermines your decisions publicly. You should:","Address it privately, align on roles, and restore consistency","Publicly confront them in the meeting","Report them to HR immediately","Ignore it to keep peace",0,"Private, role-clarifying conversation restores authority."),
 ("P","Team velocity is dropping for no clear reason. You should:","Inspect flow metrics, impediments, and capacity with the team","Push harder for more story points","Blame the developers openly","Switch frameworks immediately",0,"Metrics reveal systemic impediments."),
 ("P","A stakeholder requests a feature that conflicts with compliance. You should:","Explain the constraint and propose a compliant alternative","Build it to satisfy the request","Refuse with no explanation","Escalate to the regulator directly",0,"Compliance constraints need explained alternatives."),
 ("P","The PM must deliver bad news to stakeholders. Best approach is:","Be direct, share the facts, and present the recovery plan","Hide it until the last moment","Blame an unnamed third party","Send only a vague one-line email",0,"Candid, planned communication preserves trust."),
 ("P","A contributor feels their work is invisible. You should:","Make contributions visible and recognize them specifically","Tell them visibility does not matter","Compare them unfavorably to others","Reduce their tasks to avoid attention",0,"Recognition sustains engagement."),
 ("P","Two agile teams compete for the same scarce resource. You should:","Facilitate shared prioritization and a fair allocation rule","Give it to the loudest team","Split it evenly regardless of need","Let them race to claim it",0,"Scarcity needs transparent allocation."),
 ("P","The PM is overloaded with decisions. Effective response is to:","Delegate using clear authority limits and build team capability","Make every decision to stay in control","Escalate everything to the sponsor","Avoid decisions to reduce risk",0,"Delegation with limits scales the PM."),
 ("P","A stakeholder wants daily detailed reports. You should:","Agree a reporting cadence that meets their need without waste","Send the full raw data dump each morning","Refuse and send nothing","Report only at project end",0,"Reporting should fit the need efficiently."),

 # ===== PROCESS (41%) — 62 =====
 ("R","A critical path activity is delayed and will breach the deadline. Your best response is to:","Analyze options like fast-tracking or re-sequencing with the team","Immediately crash every activity at maximum cost","Delete the quality steps to recover time","Tell the sponsor the date is fixed regardless",0,"Schedule compression needs evaluated options, not panic."),
 ("R","A work package is over budget and behind schedule. You should first:","Determine the root cause before choosing a corrective action","Cut the scope without telling the sponsor","Add more people to the task at once","Stop the work and reopen the charter",0,"Diagnosis precedes correction."),
 ("R","The SPI is 0.85 and CPI is 0.90. This means the project is:","Behind schedule and over budget, needing corrective action","Ahead of schedule and under budget","On schedule but over budget only","Behind schedule but under budget",0,"SPI<1 behind, CPI<1 over budget."),
 ("R","A key risk materializes. Your first action is to:","Execute the agreed response plan and communicate the impact","Pretend it did not happen","Blame the risk owner publicly","Cancel the project immediately",0,"Planned responses are activated, not improvised under panic."),
 ("R","Stakeholders keep adding requests. You should:","Apply change control and assess impact before approving","Implement them immediately to please stakeholders","Reject all new requests outright","Add them silently to the backlog",0,"Change control protects scope and baseline."),
 ("R","The project scope is ambiguous. You should:","Elicit and document clear requirements with stakeholders","Assume the team knows what is needed","Copy a prior project's scope verbatim","Start building to clarify later",0,"Ambiguity is resolved through elicitation."),
 ("R","A variance exceeds the threshold in the plan. You should:","Raise it per the control process and propose action","Hide it to avoid concern","Wait until the next audit","Change the threshold secretly",0,"Thresholds trigger defined responses."),
 ("R","To estimate a complex, uncertain task you should:","Use three-point estimates with the team's input","Pick the most optimistic number","Copy last year's figure exactly","Ask the sponsor for a number",0,"Three-point estimation captures uncertainty."),
 ("R","A defect is found in a delivered component. You should:","Log it, assess impact, and route through defect repair control","Ignore it if the client has not noticed","Rework everything from scratch","Blame the developer in the meeting",0,"Defects follow a controlled repair path."),
 ("R","The schedule baseline slips due to approved changes. You should:","Re-baseline through change control when justified","Keep the old baseline and fake the reports","Never re-baseline under any condition","Discard baselines entirely",0,"Re-baselining is a controlled, justified act."),
 ("R","A vendor misses a delivery milestone. You should:","Review the contract, communicate impact, and trigger the response","Terminate the contract instantly","Do nothing since it is their problem","Pay a penalty without discussion",0,"Vendor issues use the contract and communications plan."),
 ("R","Quality audits show recurring process gaps. You should:","Update the process and training to prevent recurrence","Punish the workers responsible","Lower the quality standard","Ignore the audit findings",0,"Audits drive process improvement."),
 ("R","The team wants to adopt a new framework mid-project. You should:","Assess impact, pilot carefully, and decide with stakeholders","Switch frameworks overnight with no plan","Reject all change to the process","Copy whatever competitors use",0,"Method changes are evaluated, not impulsive."),
 ("R","Earned value shows CPI 1.05 and SPI 0.95. The project is:","Slightly under budget and slightly behind schedule","Over budget and ahead of schedule","Under budget and ahead of schedule","Over budget and behind schedule",0,"CPI>1 good, SPI<1 behind."),
 ("R","A requirement changes after design is complete. You should:","Run change control, re-estimate impact, and update baselines","Redesign everything from zero","Ignore the change request","Approve it with no analysis",0,"Late changes still follow control."),
 ("R","The risk register has many open high items. You should:","Prioritize by probability and impact and assign owners","Close them all to look good","Ignore the low ones entirely","Escalate every item to the sponsor",0,"Risks are prioritized, not mass-closed."),
 ("R","A stakeholder asks for a status not in the plan. You should:","Confirm need, then adjust the communication plan appropriately","Refuse because it is not in the plan","Send the entire raw dataset","Invent plausible numbers",0,"Communication plans adapt to needs."),
 ("R","The project is consistently late on testing. Root cause may be:","Insufficient time reserved for testing in the schedule","Lazy testers who should be replaced","Too much documentation","An over-skilled team",0,"Plan quality time, don't blame people."),
 ("R","To manage a large WBS you should:","Decompose to manageable work packages with clear ownership","Keep it at one giant level of detail","Hide the WBS from the team","Decompose to the resource level only",0,"Decomposition yields ownable packages."),
 ("R","A dependency was missed between two activities. You should:","Add the dependency, re-sequence, and re-baseline if needed","Leave it and hope it works out","Delete the second activity","Blame the scheduler",0,"Missed logic is corrected, not ignored."),
 ("R","The sponsor wants to skip user acceptance testing. You should:","Explain the value, propose a lighter UAT, and get informed sign-off","Skip UAT entirely to save time","Refuse and stop the project","Add double the testing instead",0,"UAT validates fitness for use."),
 ("R","Costs are trending over the budget baseline. You should:","Forecast with EAC, find drivers, and propose corrective action","Stop all spending immediately","Hide the trend from the sponsor","Blame inflation only",0,"Forecasts and root causes drive action."),
 ("R","A team member estimates optimistically to please you. You should:","Use range estimates and ask for their confidence and assumptions","Accept the number to keep morale","Double it without discussion","Force a pessimistic number",0,"Ranges surface uncertainty honestly."),
 ("R","The closure phase is rushed. You should:","Confirm acceptance, hand over, and capture lessons learned","Skip handover to ship faster","Archive nothing to save time","Blame the client for the rush",0,"Closure needs formal acceptance and learning."),
 ("R","A change is approved but its impact was underestimated. You should:","Re-assess, communicate the new impact, and adjust the plan","Proceed as originally scoped regardless","Cancel the change abruptly","Hide the underestimate",0,"New information triggers re-planning."),
 ("R","Quality control keeps finding the same defect. You should:","Move to quality assurance and fix the underlying process","Keep reworking each instance manually","Lower the acceptance criteria","Penalize the testers",0,"Recurring defects need process fixes."),
 ("R","The team is unsure which requirements are in scope. You should:","Point them to the requirements traceability and baseline","Tell them to use their judgement","Guess based on the newest email","Exclude everything not yet built",0,"Traceability clarifies scope."),
 ("R","A schedule risk could delay launch. You should:","Add a buffer or contingency based on analysis, not guesswork","Pad every task by 50% blindly","Ignore it since plans are fixed","Cut testing to absorb it",0,"Contingency is analysis-based."),
 ("R","Stakeholders disagree on the success criteria. You should:","Facilitate agreement on measurable criteria up front","Pick the sponsor's view silently","Use last project's criteria","Avoid defining criteria",0,"Agreed criteria prevent disputes."),
 ("R","The project has many small changes eroding the baseline. You should:","Enforce change control and review cumulative impact","Approve each one casually","Freeze all changes permanently","Ignore the erosion",0,"Creeping changes need control."),
 ("R","A resource is double-booked across projects. You should:","Clarify priorities and negotiate allocation with the managers","Let the resource decide alone","Pull them off the other project","Report the manager to HR",0,"Allocation conflicts need negotiation."),
 ("R","The CPI is 0.80 and trending down. You should:","Investigate cost drivers and act before variance grows","Wait until the end to review","Hide it from the sponsor","Increase the budget silently",0,"Early action limits cost overrun."),
 ("R","A milestone is at risk due to a dependency on another team. You should:","Coordinate the interface and track it as a key risk","Assume they will deliver on time","Remove the dependency silently","Escalate to the program office only at failure",0,"Cross-team dependencies need active coordination."),
 ("R","The scope baseline and the plan differ. You should:","Reconcile them through change control to a single source","Keep both and use whichever fits","Discard the baseline","Ignore the discrepancy",0,"One controlled baseline is essential."),
 ("R","To improve estimation accuracy you should:","Use historical data and the team's expertise iteratively","Always guess the midpoint","Copy an unrelated project","Ask the client for the estimate",0,"Estimation improves with data and iteration."),
 ("R","A defect escapes to production. You should:","Trigger incident response, fix, and update controls to prevent recurrence","Ignore it if users are quiet","Rewrite the whole system","Blame the tester publicly",0,"Escaped defects need response and learning."),
 ("R","The team wants to automate a manual control. You should:","Assess feasibility, keep oversight, and validate the automation","Automate blindly to save effort","Reject automation entirely","Automate and remove all humans",0,"Automation needs validation and oversight."),
 ("R","A schedule compression is needed. Between crashing and fast-tracking you should:","Choose based on cost, risk, and which path is safer","Always crash regardless of cost","Always fast-track regardless of risk","Pick randomly",0,"Compression methods have different trade-offs."),
 ("R","Stakeholders receive conflicting reports. Root cause is:","No single source of truth and weak communication control","A malicious team member","Bad luck","An outdated tool",0,"Controlled reporting prevents conflict."),
 ("R","The risk response for a high risk is 'avoid'. You should:","Change the plan to eliminate the threat entirely","Buy insurance and move on","Accept it and monitor","Transfer it to a vendor",0,"Avoidance removes the threat's cause."),
 ("R","A vendor proposes a cheaper change. You should:","Evaluate quality and long-term impact, not price alone","Accept it purely because it is cheap","Reject it purely because it is cheap","Ignore the proposal",0,"Value includes quality and risk."),
 ("R","The project's benefits are unclear to the team. You should:","Connect tasks to the business case and expected benefits","Keep the business case hidden","Tell them benefits do not matter","Rewrite the case without input",0,"Benefit clarity drives motivation."),
 ("R","A control limit is breached on a quality chart. You should:","Investigate the special cause before adjusting the process","Adjust the process randomly","Ignore it as noise","Stop production forever",0,"Special causes need investigation."),
 ("R","The team completes work but the sponsor will not accept it. You should:","Confirm the acceptance criteria and close the gap explicitly","Force acceptance through escalation","Rewrite the criteria silently","Accept it yourself",0,"Acceptance hinges on agreed criteria."),
 ("R","A requirement is technically infeasible. You should:","Surface it early, explore alternatives, and re-baseline if needed","Build a poor approximation anyway","Drop the feature without notice","Pretend it was delivered",0,"Infeasibility is raised, not faked."),
 ("R","To track progress credibly you should:","Use earned value and trend analysis against the baseline","Report gut feel only","Compare to a different project","Hide variance",0,"EV gives objective progress."),
 ("R","A key assumption proves false. You should:","Reassess the plan and update risks and baselines accordingly","Pretend the assumption holds","Blame the person who stated it","Abandon the project",0,"False assumptions trigger re-planning."),
 ("R","The team is gold-plating the product. You should:","Refocus them on the defined scope and value","Encourage more features always","Punish them for effort","Add the extras to scope silently",0,"Gold-plating wastes resources."),
 ("R","A risk owner reports a risk is closed but you doubt it. You should:","Verify the evidence and closure criteria before updating","Trust the word blindly","Reopen all risks","Escalate to the sponsor instantly",0,"Closure needs verification."),
 ("R","The project is behind and leadership wants a recovery plan. You should:","Analyze options, model the recovery, and present a realistic plan","Promise an impossible date","Do nothing and hope","Blame the team",0,"Recovery is planned, not wished."),
 ("R","A dependency is finish-to-finish but modeled as finish-to-start. You should:","Correct the logic to reflect the true relationship","Leave the error in the schedule","Delete the successor","Reverse the activities",0,"Schedule logic must reflect reality."),
 ("R","Quality is failing intermittently. You should:","Stabilize the process and use statistical control","Inspect 100% forever","Lower the standard","Replace all staff",0,"Stable processes yield consistent quality."),
 ("R","The team underestimates a risky task. You should:","Use a wider estimate range and add a contingency reserve","Force a single fixed date","Ignore the risk","Cut the task",0,"Risk needs range and reserve."),
 ("R","A change control board is overloaded. You should:","Tier the process and delegate within defined authority","Abolish the CCB entirely","Escalate everything to the CEO","Ignore small changes",0,"Tiered control scales governance."),
 ("R","The project's critical path has no float. You should:","Manage it closely and protect it with contingency","Ignore it since it is fine","Add float by delaying start","Remove the longest activity",0,"Zero-float paths need protection."),
 ("R","A stakeholder wants daily scope changes. You should:","Channel them through change control with impact analysis","Implement each one instantly","Reject all changes","Add them to a secret list",0,"Change control absorbs churn."),
 ("R","The estimate at completion exceeds the budget. You should:","Report the EAC, explain drivers, and propose options","Hide the EAC","Cap spending illegally","Blame the estimator",0,"Forecasts inform decisions."),
 ("R","A process tailors poorly to the project. You should:","Tailor it to the context per the methodology's guidance","Use it rigidly regardless","Abandon all process","Copy a different industry",0,"Tailoring fits context."),
 ("R","The team discovers a better technical approach mid-build. You should:","Evaluate value, risk, and impact before adopting it","Switch instantly with no review","Reject it to protect the plan","Steal the idea silently",0,"Improvements are evaluated."),
 ("R","A resource quits with no notice. You should:","Trigger the contingency, re-plan capacity, and communicate impact","Panic and stop the project","Hide the gap from the sponsor","Blame the manager",0,"Contingency and re-planning absorb shocks."),
 ("R","The quality plan lacks inspection points. You should:","Add control points at meaningful stages of the lifecycle","Inspect only at the end","Remove quality entirely","Inspect randomly with no plan",0,"Planned control points catch defects early."),
 ("R","A schedule risk could delay launch. You should:","Quantify it, add a contingency reserve, and monitor triggers","Deny the risk exists","Cut scope blindly","Escalate only at failure",0,"Risks are quantified and monitored."),
 ("R","Stakeholders dispute the priority of two deliverables. You should:","Rank them against the business case and agreed value","Pick the cheaper one","Pick the easier one","Flip a coin",0,"Priority follows value."),
 ("R","The project is over budget but on schedule. You should:","Analyze cost drivers and protect the schedule with trade-offs","Spend more to catch up","Ignore the budget","Cut scope randomly",0,"Trade-offs balance the constraints."),
 ("R","A control process is skipped under pressure. You should:","Restore it and review what slipped during the gap","Keep skipping to save time","Punish the team publicly","Document that controls are optional",0,"Controls are restored, not dropped."),

 # ===== BUSINESS ENVIRONMENT (26%) — 38 =====
 ("B","A new regulation affects your project's data handling. You should first:","Assess the impact on scope, compliance, and the plan","Ignore it since it is not technical","Ask the team to handle it quietly","Wait for the regulator to fine someone",0,"Regulatory change is a risk to assess and plan for."),
 ("B","The project's business case is no longer valid. You should:","Re-validate with sponsors and recommend continuation or closure","Keep going to avoid embarrassment","Hide the finding from sponsors","Abandon the project instantly",0,"Invalid business case triggers a go/no-go review."),
 ("B","A merger changes the project's owning organization. You should:","Re-assess stakeholders, alignment, and the business case","Assume nothing changes","Stop the project immediately","Reassign everything to the old org",0,"Org change reshapes context and value."),
 ("B","The sponsor asks you to skip a required compliance control. You should:","Explain the obligation and escalate if the pressure continues","Skip it to please the sponsor","Ignore the regulation entirely","Report the sponsor to authorities",0,"Compliance is non-negotiable; escalate appropriately."),
 ("B","To ensure benefits are realized you should:","Define measurable benefits and track them through closure","Assume benefits appear automatically","Track only the schedule","Delete the benefits section",0,"Benefits need defined, tracked measures."),
 ("B","A competitor launches a similar product first. You should:","Reassess differentiation and recommend a value review","Panic and copy their features","Cancel the project outright","Hide the news from sponsors",0,"Market change triggers re-evaluation."),
 ("B","The project's value is questioned by executives. You should:","Present the business case, metrics, and progress evidence","Argue defensively with no data","Hide the metrics","Threaten to quit",0,"Value claims need evidence."),
 ("B","An external political shift threatens funding. You should:","Monitor the environment and prepare contingency messaging","Ignore politics entirely","Publicly criticize the government","Stop reporting",0,"External factors are monitored."),
 ("B","The organization lacks maturity for your methodology. You should:","Tailor the approach and build capability incrementally","Force the full framework regardless","Abandon methodology entirely","Report the org to the PMO",0,"Maturity gaps need tailored, gradual uplift."),
 ("B","A new executive sponsor has different priorities. You should:","Re-confirm objectives and align the plan to the new priorities","Keep the old plan unchanged","Resist the new priorities","Remove the old sponsor",0,"Sponsor change requires re-alignment."),
 ("B","The project delivers on time but misses its business goal. You should:","Analyze the benefits realization gap and recommend action","Declare success regardless","Blame the business side","Hide the gap",0,"Goal miss is a benefits gap to analyze."),
 ("B","A new law requires data localization. You should:","Assess architecture impact and plan compliant changes","Ignore it as an IT detail","Move all data to a random country","Refuse to comply",0,"Legal change drives architecture impact analysis."),
 ("B","Stakeholders outside the project are affected. You should:","Identify and engage them per the stakeholder map","Ignore them since they are external","Treat them as enemies","Exclude them from all comms",0,"External stakeholders still need engagement."),
 ("B","The PMO mandates a standard you find heavy. You should:","Adopt it and suggest improvements through the right channel","Ignore the standard openly","Sabotage the standard","Quit the organization",0,"Standards are followed; improvements are proposed."),
 ("B","A social responsibility concern arises in the project. You should:","Assess the impact and choose the responsible path","Ignore it as off-topic","Hide it from stakeholders","Exploit the situation",0,"Responsibility is part of the environment."),
 ("B","Funding is reduced by 30% mid-project. You should:","Re-scope with sponsors to the new budget realistically","Spend the same and go over","Hide the cut from the team","Abandon quality",0,"Budget cuts need re-scoping with sponsors."),
 ("B","The market need the project addressed has disappeared. You should:","Recommend a formal closure or pivot decision","Keep building regardless","Hide the change","Blame the sponsor",0,"Vanished need ends the case."),
 ("B","A vendor is found to breach a labor standard. You should:","Raise it, review the contract, and require remediation","Ignore it to save cost","Switch vendors instantly","Report them to the press",0,"Ethical breaches are managed via contract."),
 ("B","The project supports a strategic objective that shifted. You should:","Re-baseline alignment to the current strategy","Keep the old objective","Ignore strategy entirely","Argue the old strategy was right",0,"Strategy shift realigns the project."),
 ("B","An economic downturn threatens the business case. You should:","Re-forecast benefits and propose a staged approach","Deny the downturn","Cancel everything","Hide the forecast",0,"Downturns require re-forecasting."),
 ("B","A community group opposes the project. You should:","Engage them, understand concerns, and address impacts","Ignore them as outsiders","Attack them publicly","Exclude them from comms",0,"Opposition needs engagement."),
 ("B","The project's ROI is below threshold at review. You should:","Present the analysis and recommend a gate decision","Hide the ROI","Inflate the numbers","Cancel without review",0,"Gate decisions use honest ROI."),
 ("B","A new industry standard emerges. You should:","Assess relevance and plan adoption where it adds value","Ignore it completely","Adopt it blindly everywhere","Mock the standard",0,"Standards are assessed for value."),
 ("B","The organization's risk appetite tightens. You should:","Re-tune responses and reserves to the new appetite","Ignore the change","Take more risk to compensate","Stop all work",0,"Appetite changes retune risk handling."),
 ("B","A partner organization changes its API you depend on. You should:","Assess the integration impact and plan the change","Assume it still works","Blame the partner publicly","Drop the integration silently",0,"External dependency change is assessed."),
 ("B","The project's success metric is vanity-based. You should:","Redefine it to a meaningful outcome with stakeholders","Keep the easy metric","Drop metrics entirely","Hide the real metric",0,"Metrics must reflect value."),
 ("B","A data breach occurs at a partner. You should:","Activate response, assess exposure, and communicate per plan","Ignore it since it is their breach","Post about it publicly","Hide it from your sponsor",0,"Partner breaches still need response."),
 ("B","The project is duplicating another internal effort. You should:","Surface the overlap and recommend consolidation","Compete with the other team","Hide the duplication","Merge without telling anyone",0,"Duplication wastes resources."),
 ("B","A new tax changes the project's cost model. You should:","Re-forecast the financials with the new assumption","Ignore tax as irrelevant","Hide the change","Inflate costs",0,"Tax changes re-forecast finances."),
 ("B","Stakeholders expect benefits sooner than realistic. You should:","Set expectations with a phased realization roadmap","Promise the impossible date","Hide the timeline","Blame the team",0,"Expectations need a realistic roadmap."),
 ("B","The project's outputs are not being adopted. You should:","Investigate adoption barriers and enable the change","Force adoption by mandate","Blame the users","Abandon the outputs",0,"Adoption needs enablement."),
 ("B","A geopolitical event disrupts a supplier. You should:","Activate the supply-risk response and seek alternatives","Ignore it as external","Blame the country","Stop the project",0,"Supply disruption uses the risk plan."),
 ("B","The business case assumed a trend that reversed. You should:","Update the assumption, re-model, and advise sponsors","Keep the old assumption","Hide the reversal","Argue the trend is fine",0,"Reverted trends re-model the case."),
 ("B","A new board mandate changes reporting. You should:","Align governance reporting to the mandate transparently","Ignore the mandate","Hide reports from the board","Resist the board",0,"Mandates reshape governance."),
 ("B","The project's environmental impact is questioned. You should:","Assess it and mitigate where feasible and required","Dismiss it as irrelevant","Hide the assessment","Exaggerate the harm",0,"Impact is assessed and mitigated."),
 ("B","A key benefit owner leaves the organization. You should:","Re-assign ownership and keep benefit tracking alive","Drop the benefit tracking","Blame the departure","Hide the gap",0,"Benefit ownership must be maintained."),
 ("B","The project is no longer strategically prioritized. You should:","Recommend a hold or reprioritization decision clearly","Keep spending regardless","Hide the reprioritization","Argue the priority is wrong",0,"Priority changes drive decisions."),
 ("B","A customer requirement conflicts with law. You should:","Explain the conflict and propose a compliant solution","Build it to satisfy the customer","Refuse with no alternative","Report the customer",0,"Law constrains; alternatives are offered."),
 ("B","The economic case depends on a fragile assumption. You should:","Identify the sensitivity and plan contingencies","Pretend the assumption is solid","Hide the fragility","Remove the assumption",0,"Fragile assumptions need sensitivity analysis."),
 ("B","A merger reduces the project's funding source. You should:","Reconfirm the business case with the new owners","Assume funding continues","Stop immediately","Hide the change",0,"Ownership change reconfirms the case."),
 ("B","The project's value is realized but undocumented. You should:","Capture and communicate the realized benefits formally","Leave them undocumented","Exaggerate them","Hide them",0,"Realized benefits are captured."),
]

Q_raw = balance(Q_raw)

# safety net: trim/pad to exactly 150
print("raw count:", len(Q_raw), "domains:", dict(Counter(q[0] for q in Q_raw)))
tgt={"P":50,"R":62,"B":38}
while len(Q_raw)>150:
    for d in ["B","R","P"]:
        for i in range(len(Q_raw)-1,-1,-1):
            if Q_raw[i][0]==d:
                del Q_raw[i]; break
        if len(Q_raw)<=150: break
while len(Q_raw)<150:
    for d in ["P","R","B"]:
        if len(Q_raw)<150 and sum(1 for q in Q_raw if q[0]==d)<tgt[d]:
            Q_raw.append((d,"A project situation requires a balanced response. The PM should:","Assess the context and apply the appropriate practice","Act without analysis to save time","Ignore the situation entirely","Escalate everything at once",0,"Situational practice beats reflex."))
            break

# balance correct positions A/B/C/D
random.seed(2026)
targets=[0,1,2,3]*(150//4)
while len(targets)<150:
    targets.append(len(targets)%4)
random.shuffle(targets)
Q=[]
for i,(dom,q,o0,o1,o2,o3,ai,exp) in enumerate(Q_raw):
    opts=[o0,o1,o2,o3]
    t=targets[i]
    shift=(ai-t)%len(opts)
    rotd=opts[shift:]+opts[:shift]
    Q.append({"d":dom,"q":q,"o":rotd,"a":t,"x":exp})
dist=[0,0,0,0]
for q in Q: dist[q["a"]]+=1
for i,(dom,q,o0,o1,o2,o3,ai,exp) in enumerate(Q_raw):
    assert Q[i]["o"][Q[i]["a"]]==[o0,o1,o2,o3][ai],"integrity fail at %d"%i
print("final:",len(Q),"domains:",dict(Counter(q["d"] for q in Q)),"dist:",dist,"INTEGRITY OK")


# ---------------- HTML builder (fixed: reveal only on click) ----------------
def jss(x): return x.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")
STUDYGUIDE = {
  "P": ["Lead with empathy and servant leadership; resolve conflict collaboratively.","Build psychological safety, inclusion, and clear norms.","Tailor stakeholder engagement and communicate two-way."],
  "R": ["Control scope, schedule, cost, quality, risk through the baseline.","Use earned value and root-cause analysis before acting.","Channel change through change control, not ad hoc edits."],
  "B": ["Tie work to the business case and realized benefits.","Monitor external factors: regulation, market, strategy, funding.","Make go/no-go decisions on honest evidence."]
}
Q_json = "[" + ",".join(
    '{"d":"%s","q":"%s","o":["%s","%s","%s","%s"],"a":%d,"x":"%s"}' % (
        q["d"], jss(q["q"]), jss(q["o"][0]), jss(q["o"][1]), jss(q["o"][2]), jss(q["o"][3]), q["a"], jss(q["x"])
    ) for q in Q
) + "]"
DOM_json = "{" + ",".join('"%s":"%s"' % (k, jss(v)) for k,v in DOMAINS.items()) + "}"
SG_json = "{" + ",".join('"%s":["%s"]' % (k, '","'.join(jss(t) for t in v)) for k,v in STUDYGUIDE.items()) + "}"

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
  <span class="pill">Project Management Professional</span>
  <span class="pill">150 questions</span>
  <span class="spacer"></span>
  <span id="progress" class="pill">Answered 0 / 150</span>
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
    <div class="big"><span id="scnum">0</span><span style="font-size:1rem;color:var(--muted)"> / 150</span></div>
    <div id="verdict" class="legend"></div>
    <div id="pie"></div>
    <div class="break" id="breakdown"></div>
    <div class="rec" id="rec"><h3>Focus area — weakest domain</h3><ul id="recul"></ul></div>
    <div id="review"></div>
  </div>
</main>

<footer>
  Self-made study companion for the PMP exam using the current PMI Exam Content Outline (People 33% / Process 41% / Business Environment 26%). Not an official PMI product.
  Real exam: 180 questions, 230 minutes. The 70% here is a self-set practice benchmark. Pair with official <a href="https://www.pmi.org/certifications/project-management-pmp" target="_blank">PMP</a> resources.
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
  document.getElementById('verdict').textContent = 'You answered '+answered+' of '+Q.length+'. Score: '+pct+'% — '+(pass?'PASS (>=70%)':'BELOW PASS (>=70%)');
  renderPie(dom,pct);
  const bd=document.getElementById('breakdown'); bd.innerHTML='';
  Object.keys(DOMAINS).forEach(k=>{
    const d=dom[k]; const p=d.t?Math.round(d.c/d.t*100):0;
    const cls = p>=PASS_PCT?'ok':'no';
    bd.innerHTML+='<div class="brow"><span>'+DOMAINS[k]+' <span style="color:var(--muted)">('+d.t+' Q)</span></span><span class="pct '+cls+'">'+d.c+'/'+d.t+' * '+p+'%</span></div>';
  });
  const rec=document.getElementById('rec'); rec.classList.add('show');
  const weakest=Object.keys(DOMAINS).map(k=>({k,p:dom[k].t?dom[k].c/dom[k].t:1})).sort((a,b)=>a.p-b.p)[0];
  const ul=document.getElementById('recul'); ul.innerHTML='';
  (STUDYGUIDE[weakest.k]||[]).forEach(t=>ul.innerHTML+='<li>'+t+'</li>');
  const rv=document.getElementById('review'); rv.innerHTML='<h3 style="margin:18px 0 8px">Review</h3>';
  Q.forEach((q,i)=>{
    const ok=answers[i]===q.a;
    rv.innerHTML+='<div class="review-item"><div class="rq">'+(i+1)+'. '+q.q+'</div>'+
      '<div class="rr '+(ok?'ok':'no')+'">'+(ok?'Correct':'Your answer: '+(answers[i]!==null?q.o[answers[i]]:'--'))+' | Correct: '+q.o[q.a]+'</div>'+
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
