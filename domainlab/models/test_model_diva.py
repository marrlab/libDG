import torch
from domainlab.algos.observers.b_obvisitor import ObVisitor
from domainlab.models.model_diva import ModelDIVA
from domainlab.utils.utils_classif import mk_dummy_label_list_str
from domainlab.compos.vae.utils_request_chain_builder import VAEChainNodeGetter
from domainlab.compos.pcr.request import RequestVAEBuilderCHW
from domainlab.dsets.dset_poly_domains_mnist_color_default import DsetMNISTColorMix
from domainlab.algos.trainers.train_visitor import TrainerVisitor
from domainlab.compos.exp.exp_main import Exp
from domainlab.arg_parser import mk_parser_main
from domainlab.utils.test_img import mk_rand_xyd
from domainlab.utils.utils_classif import mk_dummy_label_list_str




def test_model_diva():
    parser = mk_parser_main()
    margs = parser.parse_args()
    margs.nname = "conv_bn_pool_2"
    y_dim = 10
    d_dim = 2
    list_str_y = mk_dummy_label_list_str("class", y_dim)
    list_str_d = mk_dummy_label_list_str("domain", d_dim)
    request = RequestVAEBuilderCHW(3, 28, 28, args=margs)

    node = VAEChainNodeGetter(request)()
    model = ModelDIVA(node, zd_dim=8, zy_dim=8, zx_dim=8, list_d_tr=list_str_d, list_str_y=list_str_y, gamma_d=1.0, gamma_y=1.0,
                      beta_d=1.0, beta_y=1.0, beta_x=1.0)
    imgs, y_s, d_s = mk_rand_xyd(28, y_dim, 2, 2)
    one_hot, mat_prob, label, confidence, na = model.infer_y_vpicn(imgs)
    model(imgs, y_s, d_s)
